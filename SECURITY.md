# Security Guide for Image-Gen-Skill

## API Key Storage

### Current Implementation

API keys are stored in `.env` file with the following security measures:

1. **File Isolation**: Keys are NEVER hardcoded in source code
2. **Git Exclusion**: `.env` is in `.gitignore` (never committed)
3. **File Permissions**: `.env` should be `600` (owner read/write only)
4. **Runtime Loading**: Keys loaded from `.env` into environment variables

### File Structure

```
skills/image-gen-skill/
├── .env                  # API keys (600 permissions, gitignored)
├── .env.example          # Template showing required variables
├── .gitignore           # Excludes .env, *.key, secrets/
├── generate.py          # Loads key from env var
├── generate_zhipu.py    # Loads key from env var
└── SECURITY.md          # This file
```

### Required Environment Variables

```bash
# SiliconFlow
SILICONFLOW_API_KEY=sk-...

# Zhipu AI
ZHIPU_API_KEY=...
```

## Security Checklist

- [ ] `.env` file exists with correct keys
- [ ] `.env` permissions are 600 (`chmod 600 .env`)
- [ ] `.env` is in `.gitignore`
- [ ] No keys in source code
- [ ] No keys in git history (`git log -p | grep -i api_key`)
- [ ] Error messages don't expose keys

## Key Leak Prevention

### What NOT to do

❌ Hardcode keys in Python files
❌ Commit .env to GitHub
❌ Share .env file with others
❌ Log API keys to console/files
❌ Include keys in error messages

### What TO do

✅ Use .env file with restricted permissions
✅ Load keys via `os.environ` at runtime
✅ Use .env.example as template
✅ Check file permissions on startup
✅ Mask keys in logs (`sk-****...`)

## Incident Response

If you suspect a key has been leaked:

1. **Revoke immediately**: Log into platform and delete/regenerate the key
2. **Check logs**: Search for key in `git log`, shell history, log files
3. **Scan repositories**: Use GitHub's secret scanning if public
4. **Rotate keys**: Generate new keys and update .env
5. **Check usage**: Review API dashboard for unauthorized usage

## Platform-Specific Rotation

### SiliconFlow
1. Login: https://cloud.siliconflow.cn
2. Go to: API Keys → Manage
3. Delete old key, create new one
4. Update `.env` with new key

### Zhipu AI
1. Login: https://open.bigmodel.cn
2. Go to: API Keys
3. Revoke old key, create new one
4. Update `.env` with new key

## Code Review Checklist

Before accepting PRs/changes:

- [ ] No `api_key = "sk-..."` patterns in code
- [ ] No `.env` file in git diff
- [ ] No print statements showing keys
- [ ] Error handlers don't echo keys

## Contact

If you discover a security vulnerability:
- Do NOT open a public issue
- Contact: [your contact info]