#!/bin/bash

# Check if the directories exist before attempting to remove them
if [ -d "build" ]; then
    rm -r build/
fi

if [ -d "dist" ]; then
    rm -r dist/
fi

if [ -d "vid_stream.egg-info" ]; then
    rm -r vid_stream.egg-info/
fi

# Determine the site-packages directory dynamically
PYTHON_SITE_PACKAGES=$(python3 -c "import site; print(site.getsitepackages()[0])")

# Navigate to the site-packages directory
cd "$PYTHON_SITE_PACKAGES" || {
    echo "Failed to navigate to $PYTHON_SITE_PACKAGES directory"
    exit 1
}

# Check if any of the vid_stream egg files exist before attempting to remove them
# Remove all vid_stream egg files
for file in vid_stream-0.0.1-*.egg; do
    if [ -e "$file" ]; then
        rm -r "$file"
    fi
done
