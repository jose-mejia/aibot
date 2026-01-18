#!/usr/bin/env python3
"""
Script to create GitHub Issues for MT5 Connection Flow implementation
"""
import requests
import json
import sys

# GitHub API configuration
GITHUB_API = "https://api.github.com"
OWNER = "jose-mejia"

# Repository names
REPOS = ["master_sender", "client_copier"]

# Issue content for Master Sender
MASTER_ISSUE = {
    "title": "Implement Strict MT5 Connection Flow with Security Validation",
    "body": """## 🎯 Objective
Implement the strict MT5 connection flow as documented in `FLOW_MT5_CONNECTION.md` to ensure the Master Sender only connects to the authorized MT5 account.

## 📋 Background
Currently, the Master Sender may connect to any available MT5 terminal. This creates a security risk where it could monitor the wrong account if multiple MT5 instances are open.

## 🔒 Security Principles (Must Implement)
1. **Single Source of Truth:** Connection parameters (`mt5_id` and `mt5_path`) MUST come from the API/Database
2. **Fail Fast:** Abort immediately if connection data is incomplete or null
3. **Strict Path:** Use `mt5.initialize(path=DB_PATH)` - no "Observer Mode" in production
4. **Identity Validation:** Verify `mt5.account_info().login` matches expected `mt5_id` - activate Kill Switch if mismatch

## 🛠️ Implementation Tasks
- [ ] Fetch `mt5_path` and `allowed_mt5_id` from API endpoint `/users/me`
- [ ] Add validation: abort if either value is null/empty
- [ ] Update `mt5.initialize()` to use explicit path parameter
- [ ] Add post-connection identity check
- [ ] Implement Kill Switch: `mt5.shutdown()` + `sys.exit(1)` on mismatch
- [ ] Add CRITICAL level logging for all security failures
- [ ] Update error messages to be clear about security violations

## 📝 Code Reference
File: `sender_service.py` or `mt5_connector.py`

Expected flow:
```python
# 1. Fetch from API
user_data = api.get_profile()
required_login = user_data['allowed_mt5_id']
required_path = user_data['mt5_path']

# 2. Validate prerequisites
if not required_login or not required_path:
    logger.critical("SECURITY: MT5 credentials not found. Aborting.")
    sys.exit(1)

# 3. Directed connection
if not mt5.initialize(path=required_path):
    logger.critical(f"Failed to initialize MT5 at: {required_path}")
    sys.exit(1)

# 4. Identity validation (The Guardian)
current_info = mt5.account_info()
if current_info.login != int(required_login):
    logger.critical(f"FATAL: Wrong Account! Expected: {required_login}, Found: {current_info.login}")
    mt5.shutdown()
    sys.exit(1)  # Kill Switch
```

## ✅ Acceptance Criteria
- [ ] Master Sender refuses to start if `mt5_path` is not configured in database
- [ ] Master Sender connects only to the MT5 terminal at the specified path
- [ ] Master Sender terminates immediately if connected account ID doesn't match expected ID
- [ ] All security failures generate CRITICAL logs
- [ ] Manual testing confirms connection to correct account (7409735)

## 🔗 Related Documentation
- `docs/flows/FLOW_MT5_CONNECTION.md`
- `docs/WORKFLOW_MT5_PATH.md`
- `docs/devia/CHAT_TRANSCRIPT_2026_01_04.md` (Context of "Wrong Account" bug)

## 🏷️ Labels
`security`, `critical`, `mt5-connection`, `enhancement`

## 📌 Priority
**Critical** - This is a security requirement to prevent monitoring wrong accounts
""",
    "labels": ["security", "critical", "mt5-connection", "enhancement"]
}

# Issue content for Client Copier (similar but adapted)
CLIENT_ISSUE = {
    "title": "Implement Strict MT5 Connection Flow with Security Validation",
    "body": """## 🎯 Objective
Implement the strict MT5 connection flow as documented in `FLOW_MT5_CONNECTION.md` to ensure the Client Copier only connects to the authorized MT5 account.

## 📋 Background
Currently, the Client Copier may connect to any available MT5 terminal. This creates a security risk where it could execute trades on the wrong account if multiple MT5 instances are open.

## 🔒 Security Principles (Must Implement)
1. **Single Source of Truth:** Connection parameters (`mt5_id` and `mt5_path`) MUST come from the API/Database
2. **Fail Fast:** Abort immediately if connection data is incomplete or null
3. **Strict Path:** Use `mt5.initialize(path=DB_PATH)` - no "Observer Mode" in production
4. **Identity Validation:** Verify `mt5.account_info().login` matches expected `mt5_id` - activate Kill Switch if mismatch

## 🛠️ Implementation Tasks
- [ ] Fetch `mt5_path` and `allowed_mt5_id` from API endpoint `/users/me`
- [ ] Add validation: abort if either value is null/empty
- [ ] Update `mt5.initialize()` to use explicit path parameter
- [ ] Add post-connection identity check
- [ ] Implement Kill Switch: `mt5.shutdown()` + `sys.exit(1)` on mismatch
- [ ] Add CRITICAL level logging for all security failures
- [ ] Update error messages to be clear about security violations

## 📝 Code Reference
File: `client_service.py` or `mt5_connector.py`

Expected flow:
```python
# 1. Fetch from API
user_data = api.get_profile()
required_login = user_data['allowed_mt5_id']
required_path = user_data['mt5_path']

# 2. Validate prerequisites
if not required_login or not required_path:
    logger.critical("SECURITY: MT5 credentials not found. Aborting.")
    sys.exit(1)

# 3. Directed connection
if not mt5.initialize(path=required_path):
    logger.critical(f"Failed to initialize MT5 at: {required_path}")
    sys.exit(1)

# 4. Identity validation (The Guardian)
current_info = mt5.account_info()
if current_info.login != int(required_login):
    logger.critical(f"FATAL: Wrong Account! Expected: {required_login}, Found: {current_info.login}")
    mt5.shutdown()
    sys.exit(1)  # Kill Switch
```

## ✅ Acceptance Criteria
- [ ] Client Copier refuses to start if `mt5_path` is not configured in database
- [ ] Client Copier connects only to the MT5 terminal at the specified path
- [ ] Client Copier terminates immediately if connected account ID doesn't match expected ID
- [ ] All security failures generate CRITICAL logs
- [ ] Manual testing confirms connection to correct account (11629107)

## 🔗 Related Documentation
- `docs/flows/FLOW_MT5_CONNECTION.md`
- `docs/WORKFLOW_MT5_PATH.md`
- `docs/devia/CHAT_TRANSCRIPT_2026_01_04.md` (Context of "Wrong Account" bug)

## 🏷️ Labels
`security`, `critical`, `mt5-connection`, `enhancement`

## 📌 Priority
**Critical** - This is a security requirement to prevent executing trades on wrong accounts
""",
    "labels": ["security", "critical", "mt5-connection", "enhancement"]
}

def get_github_token():
    """Try to get GitHub token from git credential helper"""
    import subprocess
    try:
        # Try to get token from git credential helper
        result = subprocess.run(
            ['git', 'config', '--global', 'github.token'],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        
        # If not found, prompt user
        print("GitHub token not found in git config.")
        print("Please provide a GitHub Personal Access Token with 'repo' scope:")
        token = input("Token: ").strip()
        return token
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

def create_issue(repo, issue_data, token):
    """Create a GitHub issue"""
    url = f"{GITHUB_API}/repos/{OWNER}/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.post(url, headers=headers, json=issue_data)
    
    if response.status_code == 201:
        issue = response.json()
        print(f"✅ Created issue #{issue['number']} in {repo}")
        print(f"   URL: {issue['html_url']}")
        return True
    else:
        print(f"❌ Failed to create issue in {repo}")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def main():
    print("🚀 Creating GitHub Issues for MT5 Connection Flow\n")
    
    # Get GitHub token
    token = get_github_token()
    if not token:
        print("❌ No GitHub token provided. Exiting.")
        sys.exit(1)
    
    # Create issues
    issues_data = {
        "master_sender": MASTER_ISSUE,
        "client_copier": CLIENT_ISSUE
    }
    
    success_count = 0
    for repo in REPOS:
        print(f"\n📝 Creating issue in {repo}...")
        if create_issue(repo, issues_data[repo], token):
            success_count += 1
    
    print(f"\n✨ Done! Created {success_count}/{len(REPOS)} issues successfully.")

if __name__ == "__main__":
    main()
