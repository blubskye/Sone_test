#!/bin/bash
# Build script for Sone plugin
# This compiles the plugin and creates a JAR with all dependencies

set -e

# Use Java 21 (Kotlin doesn't support Java 25 yet)
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk
export PATH="$JAVA_HOME/bin:$PATH"

echo "Building Sone plugin..."
echo "Using Java: $(java -version 2>&1 | head -1)"

# Stop any existing Gradle daemons that might be using wrong Java version
./gradlew --stop 2>/dev/null || true

# Run the Gradle build (skip tests for faster build, no daemon to avoid version issues)
./gradlew fatJar -x test -x parallelTest -x notParallelTest --no-daemon

echo ""
echo "Build complete!"
echo "The plugin JAR is located at:"
echo "  build/libs/sone-jar-with-dependencies.jar"
echo ""
echo "To install in Freenet:"
echo "  1. Copy the JAR to your Freenet plugins directory"
echo "  2. Or load it via the Freenet web interface under Plugins"
