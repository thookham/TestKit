# TestKit Profile: None None
# OS: None
# Hardware: None Cores, 8192MB RAM

FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Set Environment Variables to simulate hardware specs
ENV TESTKIT_PROFILE_ID="framework-laptop-13-(intel-13th-gen)-windows-11-v1"
ENV TESTKIT_MAKE="None"
ENV TESTKIT_MODEL="None"
ENV TESTKIT_CPU_CORES="None"
ENV TESTKIT_RAM_MB="8192"
ENV TESTKIT_GPU_VRAM_MB="0"
ENV TESTKIT_RESOLUTION="2256x1504"

# Placeholder for actual simulation logic
RUN echo "Initializing TestKit Environment for framework-laptop-13-(intel-13th-gen)-windows-11-v1"
