# TestKit Profile: None None
# OS: None
# Hardware: None Cores, 2048MB RAM

FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Set Environment Variables to simulate hardware specs
ENV TESTKIT_PROFILE_ID="raspberry-pi-4-model-b-windows-11-v109"
ENV TESTKIT_MAKE="None"
ENV TESTKIT_MODEL="None"
ENV TESTKIT_CPU_CORES="None"
ENV TESTKIT_RAM_MB="2048"
ENV TESTKIT_GPU_VRAM_MB="0"
ENV TESTKIT_RESOLUTION="1920x1080"

# Placeholder for actual simulation logic
RUN echo "Initializing TestKit Environment for raspberry-pi-4-model-b-windows-11-v109"
