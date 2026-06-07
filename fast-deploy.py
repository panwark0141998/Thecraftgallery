import os
import zipfile
import socket
import urllib.request
import urllib.error
import json

# Setup DNS lookup override for api.netlify.com to avoid network/DNS issues on this host
orig_getaddrinfo = socket.getaddrinfo
def custom_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    try:
        return orig_getaddrinfo(host, port, family, type, proto, flags)
    except socket.gaierror as e:
        if host == 'api.netlify.com':
            print(f"[DNS Override] DNS lookup failed for {host}. Redirecting to 3.19.156.32...")
            # Resolve using the static Netlify API IP
            try:
                return orig_getaddrinfo('3.19.156.32', port, socket.AF_INET, type, proto, flags)
            except Exception as inner_e:
                print(f"[DNS Override] Fallback IP resolution also failed: {inner_e}")
                raise e
        raise e

socket.getaddrinfo = custom_getaddrinfo

def main():
    site_id = "7c073a3d-39ad-4768-aac2-a3091090fcdc"
    token = "nfc_i9TraBhGLuR97mdzT5ZeVoNLR6MmuiWi343b"
    dist_dir = "dist"
    zip_path = "dist.zip"
    
    print(f"1. Zipping directory '{dist_dir}' into '{zip_path}'...")
    if not os.path.exists(dist_dir):
        print(f"[ERROR] Directory '{dist_dir}' does not exist. Please run npm run build first.")
        return
        
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_dir)
                zipf.write(file_path, arcname)
        
        # Include Netlify functions if present
        funcs_dir = "netlify"
        if os.path.exists(funcs_dir):
            print("Including Netlify functions in deployment zip...")
            for root, dirs, files in os.walk(funcs_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, ".")
                    zipf.write(file_path, arcname)
                    
        # Include netlify.toml if present
        toml_path = "netlify.toml"
        if os.path.exists(toml_path):
            print("Including netlify.toml in deployment zip...")
            zipf.write(toml_path, "netlify.toml")
                
    zip_size = os.path.getsize(zip_path)
    print(f"Zip created successfully: {zip_path} ({zip_size / 1024:.2f} KB)")
    
    print(f"2. Deploying to Netlify site {site_id}...")
    url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/zip",
        "User-Agent": "FastDeployScript/1.0"
    }
    
    try:
        with open(zip_path, "rb") as f:
            zip_data = f.read()
            
        req = urllib.request.Request(url, data=zip_data, headers=headers, method="POST")
        
        print("Sending ZIP payload to Netlify API (this bypasses CLI polling and is extremely fast)...")
        with urllib.request.urlopen(req, timeout=60) as response:
            resp_data = response.read().decode('utf-8')
            resp_json = json.loads(resp_data)
            
            deploy_id = resp_json.get("id")
            deploy_state = resp_json.get("state")
            deploy_url = resp_json.get("deploy_ssl_url") or resp_json.get("url")
            
            print("\n===================================================")
            print("  DEPLOYMENT SUCCESSFUL!")
            print("===================================================")
            print(f"Deploy ID:    {deploy_id}")
            print(f"Deploy State: {deploy_state}")
            print(f"Deploy URL:   {deploy_url}")
            print("===================================================\n")
            
            # Clean up zip file
            try:
                os.remove(zip_path)
                print("Temporary zip file cleaned up.")
            except Exception:
                pass
                
    except urllib.error.HTTPError as e:
        print(f"\n[ERROR] HTTP Error {e.code} during deployment:")
        try:
            err_details = e.read().decode('utf-8')
            print(err_details)
        except Exception:
            print(e.reason)
    except Exception as e:
        print(f"\n[ERROR] Deployment failed: {e}")

if __name__ == "__main__":
    main()
