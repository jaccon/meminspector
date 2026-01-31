# Homebrew Installation Guide

## Quick Install

```bash
brew install jaccon/tap/meminspector
```

## Setup Your Homebrew Tap (One-time setup)

If you haven't published your formula yet, follow these steps:

### 1. Create a Homebrew Tap Repository

```bash
# Create a new repository on GitHub named: homebrew-tap
# URL will be: https://github.com/jaccon/homebrew-tap
```

### 2. Clone and Setup the Tap

```bash
git clone https://github.com/jaccon/homebrew-tap.git
cd homebrew-tap

# Copy the formula
cp /path/to/meminspector/meminspector.rb Formula/meminspector.rb

# Commit and push
git add Formula/meminspector.rb
git commit -m "Add meminspector formula"
git push origin main
```

### 3. Create a Release Tag for MemInspector

Before the formula works, you need to create a release:

```bash
cd /path/to/meminspector

# Create and push tag
git tag -a v2.0.0 -m "Release v2.0.0 - Python version with graphs"
git push origin v2.0.0
```

### 4. Update the Formula SHA256

After creating the release, GitHub will generate a `.tar.gz` file:

```bash
# Download and get SHA256
wget https://github.com/jaccon/meminspector/archive/refs/tags/v2.0.0.tar.gz
shasum -a 256 v2.0.0.tar.gz
```

Copy the SHA256 hash and update it in `meminspector.rb`:

```ruby
sha256 "YOUR_SHA256_HASH_HERE"
```

### 5. Test the Formula

```bash
# Add your tap
brew tap jaccon/tap

# Install
brew install jaccon/tap/meminspector

# Test
meminspector --tui
```

### 6. Update the Formula

When you release a new version:

```bash
# Update version and SHA256 in meminspector.rb
# Commit and push to homebrew-tap repository
```

## Formula Structure

The formula is located at: `meminspector.rb`

Key components:
- **url**: Points to GitHub release tarball
- **sha256**: Checksum of the tarball (must match)
- **dependencies**: Python 3.11
- **resources**: All Python packages (psutil, rich, matplotlib, etc.)

## Troubleshooting

### Formula doesn't work

```bash
# Uninstall and reinstall
brew uninstall meminspector
brew untap jaccon/tap
brew tap jaccon/tap
brew install jaccon/tap/meminspector
```

### Update not working

```bash
# Force update
brew update
brew upgrade jaccon/tap/meminspector
```

## Resources

- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Python Formula Guide](https://docs.brew.sh/Python-for-Formula-Authors)
- [Creating Taps](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap)
