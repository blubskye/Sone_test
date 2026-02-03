#!/bin/bash
# Debug build script for Sone plugin
# Compiles with full debug info and stack traces

set -e

# Use Java 21 (Kotlin doesn't support Java 25 yet)
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk
export PATH="$JAVA_HOME/bin:$PATH"

echo "Building Sone plugin (DEBUG mode)..."
echo "Using Java: $(java -version 2>&1 | head -1)"

# Stop any existing Gradle daemons
./gradlew --stop 2>/dev/null || true

# Run the Gradle build with debug flags
./gradlew fatJar -x test -x parallelTest -x notParallelTest \
    --no-daemon \
    --stacktrace \
    --info \
    -Dorg.gradle.debug=false \
    -Dkotlin.compiler.execution.strategy=in-process

echo ""
echo "Debug build complete!"
echo "The plugin JAR is located at:"
echo "  build/libs/sone-jar-with-dependencies.jar"
