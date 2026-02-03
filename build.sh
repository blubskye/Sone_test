#!/bin/bash
# Build script for Sone plugin
# This compiles the plugin and creates a JAR with all dependencies

set -e

echo "Building Sone plugin..."

# Run the Gradle build
./gradlew fatJar

echo ""
echo "Build complete!"
echo "The plugin JAR is located at:"
echo "  build/libs/sone-jar-with-dependencies.jar"
echo ""
echo "To install in Freenet:"
echo "  1. Copy the JAR to your Freenet plugins directory"
echo "  2. Or load it via the Freenet web interface under Plugins"
