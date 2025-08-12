#!/usr/bin/env python3
"""
Test script to verify environment variable loading
"""

import os
import sys

# Add project to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Successfully loaded .env file")
except ImportError:
    print("⚠️  python-dotenv not installed")

# Check required environment variables
required_vars = [
    'PYGEOAPI_CONFIG',
    'PYGEOAPI_OPENAPI', 
    'PYGEOAPI_HOME'
]

print("\n🔍 Environment Variable Check:")
print("-" * 40)

all_good = True
for var in required_vars:
    value = os.environ.get(var)
    if value:
        print(f"✅ {var}: {value}")
        # Check if file exists
        if var in ['PYGEOAPI_CONFIG', 'PYGEOAPI_OPENAPI']:
            if os.path.exists(value):
                print(f"   📄 File exists: {value}")
            else:
                print(f"   ❌ File not found: {value}")
                all_good = False
    else:
        print(f"❌ {var}: NOT SET")
        all_good = False

print("-" * 40)

if all_good:
    print("✅ All environment variables are properly configured!")
    
    # Try to import pygeoapi components
    try:
        from pygeoapi.config import get_config
        print("✅ Successfully imported pygeoapi.config")
        
        config = get_config()
        print(f"✅ Successfully loaded config: {len(config)} sections")
        
    except Exception as e:
        print(f"❌ Failed to load pygeoapi config: {e}")
        
else:
    print("❌ Some environment variables are missing or invalid")
    print("\n💡 To fix this:")
    print("1. Make sure .env file exists in project root")
    print("2. Run: export PYGEOAPI_CONFIG=/path/to/your/pygeoapi-config.yml")
    print("3. Check file paths are correct and files exist")

# Test basic imports
print("\n🔍 Testing pygeoapi imports:")
try:
    from pygeoapi.api import API
    print("✅ Successfully imported pygeoapi.api.API")
except Exception as e:
    print(f"❌ Failed to import API: {e}")

try:
    from pygeoapi.util import get_api_rules
    print("✅ Successfully imported pygeoapi.util")
except Exception as e:
    print(f"❌ Failed to import util: {e}")
