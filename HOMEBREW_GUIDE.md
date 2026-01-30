# Homebrew Installation Guide for MemInspector

This guide explains how to prepare and publish MemInspector as a Homebrew package.

## Prerequisites

1. **GitHub Repository**: You need a public GitHub repository
2. **Git Tags**: Create version tags for releases
3. **Homebrew**: Installed on your system

## Step-by-Step Guide

### 1. Prepare Your Repository

First, ensure your repository has all necessary files:
- `meminspector.py` - Main application
- `setup.py` - Python package configuration
- `requirements.txt` - Python dependencies
- `README.md` - Documentation
- `LICENSE` - License file (MIT recommended)

### 2. Create a Release on GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Add your remote repository
git remote add origin https://github.com/yourusername/meminspector.git

# Push to GitHub
git branch -M main
git push -u origin main

# Create and push a version tag
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

### 3. Get the SHA256 Hash

After creating the release, download the source tarball and calculate its SHA256:

```bash
# Download the tarball
curl -L https://github.com/yourusername/meminspector/archive/refs/tags/v1.0.0.tar.gz -o meminspector-1.0.0.tar.gz

# Calculate SHA256
shasum -a 256 meminspector-1.0.0.tar.gz
```

### 4. Update the Formula File

Edit `meminspector.rb` and update:

1. **URL**: Replace `yourusername` with your actual GitHub username
2. **SHA256**: Replace `YOUR_SHA256_HASH_HERE` with the hash from step 3
3. **Homepage**: Update with your repository URL
4. **Resource URLs**: Update Python package versions if needed

### 5. Test the Formula Locally

```bash
# Install from local formula
brew install --build-from-source ./meminspector.rb

# Test the installation
meminspector --help

# Uninstall for testing
brew uninstall meminspector
```

### 6. Publish to Homebrew

You have two options:

#### Option A: Create a Tap (Recommended for personal projects)

```bash
# Create a tap repository on GitHub named "homebrew-tap"
# Repository structure:
# homebrew-tap/
# └── Formula/
#     └── meminspector.rb

# Users can then install with:
brew tap yourusername/tap
brew install meminspector
```

#### Option B: Submit to Homebrew Core

For submission to the official Homebrew repository:

1. Fork [homebrew-core](https://github.com/Homebrew/homebrew-core)
2. Add your formula to `Formula/m/meminspector.rb`
3. Follow [Homebrew's contribution guidelines](https://docs.brew.sh/How-To-Open-a-Homebrew-Pull-Request)
4. Submit a pull request

### 7. Create a Homebrew Tap Repository

```bash
# Create a new repository on GitHub: homebrew-tap
mkdir homebrew-tap
cd homebrew-tap

# Create Formula directory
mkdir Formula
cp /path/to/meminspector.rb Formula/

# Initialize and push
git init
git add .
git commit -m "Add meminspector formula"
git remote add origin https://github.com/yourusername/homebrew-tap.git
git branch -M main
git push -u origin main
```

## Installation Instructions for Users

Once published, users can install with:

### From Your Tap:
```bash
brew tap yourusername/tap
brew install meminspector
```

### Or directly:
```bash
brew install yourusername/tap/meminspector
```

## Updating the Formula

When you release a new version:

```bash
# Create new tag
git tag -a v1.1.0 -m "Version 1.1.0"
git push origin v1.1.0

# Calculate new SHA256
curl -L https://github.com/yourusername/meminspector/archive/refs/tags/v1.1.0.tar.gz | shasum -a 256

# Update meminspector.rb with new version and SHA256
# Commit and push to homebrew-tap repository
```

## Formula Template Explanation

```ruby
class Meminspector < Formula
  # Formula class name (capitalized, no hyphens)
  
  desc "Short description"
  homepage "Project homepage"
  url "Source tarball URL"
  sha256 "Tarball checksum"
  license "License type"

  depends_on "python@3.11"  # Dependencies

  # Python package resources
  resource "package-name" do
    url "PyPI package URL"
    sha256 "Package checksum"
  end

  def install
    virtualenv_install_with_resources  # Standard Python install
  end

  def test
    system "#{bin}/meminspector", "--help"  # Basic test
  end
end
```

## Useful Commands

```bash
# Audit your formula
brew audit --strict --online meminspector.rb

# Test formula installation
brew install --build-from-source --verbose --debug meminspector.rb

# Test formula
brew test meminspector

# Uninstall
brew uninstall meminspector
```

## Resources

- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Python for Formula Authors](https://docs.brew.sh/Python-for-Formula-Authors)
- [How to Create Homebrew Tap](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap)

## Checklist

- [ ] Repository created on GitHub
- [ ] All files committed and pushed
- [ ] Version tag created and pushed
- [ ] SHA256 hash calculated
- [ ] Formula file updated with correct URLs and hash
- [ ] Formula tested locally
- [ ] Tap repository created (if applicable)
- [ ] Formula published to tap
- [ ] Installation instructions added to main README

## Common Issues

### Issue: "SHA256 mismatch"
**Solution**: Recalculate the SHA256 hash and update the formula

### Issue: "Python dependencies not found"
**Solution**: Add missing dependencies as resources in the formula

### Issue: "Command not found after install"
**Solution**: Check the `entry_points` in setup.py matches the formula

## Next Steps

After setting up Homebrew installation, consider:
1. Adding to other package managers (pip, MacPorts)
2. Creating pre-built binaries
3. Setting up CI/CD for automatic releases
