import re
from pathlib import Path

html_path = Path("frontend/index.html")
content = html_path.read_text(encoding="utf-8")

# Add helper function getAuthHeaders
auth_helper = """
    function getAuthHeaders(extra = {}) {
      let token = localStorage.getItem("baddgroup_auth_token");
      if (!token) {
        const match = document.cookie.match(/baddgroup_token=([^;]+)/);
        if (match) token = match[1];
      }
      const headers = { ...extra };
      if (token) headers["Authorization"] = `Bearer ${token}`;
      return headers;
    }
"""

if "function getAuthHeaders" not in content:
    content = content.replace("let currentFilterClass = '';", auth_helper + "\n    let currentFilterClass = '';")

# Replace loadCameras fetch
content = re.sub(
    r'const token = localStorage\.getItem\("baddgroup_auth_token"\);\s*const res = await fetch\(\'/api/cameras\',\s*\{\s*headers:\s*token\s*\?\s*\{\s*"Authorization":\s*`Bearer \$\{token\}`\s*\}\s*:\s*\{\}\s*\}\);',
    r"const res = await fetch('/api/cameras', { headers: getAuthHeaders(), credentials: 'include' });",
    content
)

# Replace updateStatus fetch
content = re.sub(
    r'const token = localStorage\.getItem\("baddgroup_auth_token"\);\s*const res = await fetch\(\'/api/status\',\s*\{\s*headers:\s*token\s*\?\s*\{\s*"Authorization":\s*`Bearer \$\{token\}`\s*\}\s*:\s*\{\}\s*\}\);',
    r"const res = await fetch('/api/status', { headers: getAuthHeaders(), credentials: 'include' });",
    content
)

# Replace loadEvents fetch
content = re.sub(
    r'const token = localStorage\.getItem\("baddgroup_auth_token"\);\s*const res = await fetch\(url,\s*\{\s*headers:\s*token\s*\?\s*\{\s*"Authorization":\s*`Bearer \$\{token\}`\s*\}\s*:\s*\{\}\s*\}\);',
    r"const res = await fetch(url, { headers: getAuthHeaders(), credentials: 'include' });",
    content
)

# Replace initAuthAndApp fetch
content = re.sub(
    r'const token = localStorage\.getItem\("baddgroup_auth_token"\);\s*try\s*\{\s*const authRes = await fetch\("/api/auth/me",\s*\{\s*headers:\s*token\s*\?\s*\{\s*"Authorization":\s*`Bearer \$\{token\}`\s*\}\s*:\s*\{\}\s*\}\);',
    r"try {\n        const authRes = await fetch('/api/auth/me', { headers: getAuthHeaders(), credentials: 'include' });",
    content
)

html_path.write_text(content, encoding="utf-8")
print("getAuthHeaders injected and fetches updated successfully.")
