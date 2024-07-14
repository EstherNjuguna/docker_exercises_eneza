FROM ubuntu

WORKDIR /hello

COPY hello.sh .

# Make the script executable
RUN chmod +x hello.sh

# Specify the command to run when the container starts
CMD ["./hello.sh"]