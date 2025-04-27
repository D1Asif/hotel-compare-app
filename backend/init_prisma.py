import subprocess
import os
import sys

def init_prisma():
    try:
        # Create prisma directory if it doesn't exist
        if not os.path.exists("prisma"):
            os.makedirs("prisma")
        
        # Check if Prisma CLI is installed
        try:
            subprocess.run(["prisma", "--version"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("Error: Prisma CLI is not installed. Please run: npm install -g prisma")
            sys.exit(1)
        
        # Initialize Prisma if not already initialized
        if not os.path.exists("prisma/schema.prisma"):
            subprocess.run(["prisma", "init"], check=True)
        
        # Generate Prisma client
        print("Generating Prisma client...")
        subprocess.run(["prisma", "generate"], check=True)
        
        # Push the schema to the database
        print("Pushing schema to database...")
        subprocess.run(["prisma", "db", "push"], check=True)
        
        print("Prisma setup completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during Prisma setup: {e.stderr.decode() if e.stderr else e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    init_prisma() 