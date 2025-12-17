import subprocess
import tempfile
import os
import time
from django.conf import settings

def run_in_sandbox(code, language):
    """
    Run code inside a Docker container for security.
    """
    # Map languages to file extensions and commands
    config = {
        'python': {'ext': '.py', 'cmd': ['python3']},
        'javascript': {'ext': '.js', 'cmd': ['node']},
        'ruby': {'ext': '.rb', 'cmd': ['ruby']},
        'php': {'ext': '.php', 'cmd': ['php']},
        'go': {'ext': '.go', 'cmd': ['go', 'run']},
        'java': {'ext': '.java', 'cmd': ['java']},  # Simplified for single file
        'cpp': {'ext': '.cpp', 'cmd': 'g++ -o /tmp/out {file} && /tmp/out'}, # Needs shell
        'csharp': {'ext': '.cs', 'cmd': 'mcs -out:/tmp/out.exe {file} && mono /tmp/out.exe'}, # Needs shell
    }
    
    if language not in config:
        return "", f"Language '{language}' is not supported in the sandbox yet."

    lang_config = config[language]
    ext = lang_config['ext']
    
    # Create a temporary file on the host
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext, mode='w', encoding='utf-8') as temp_file:
        temp_file.write(code)
        host_file_path = temp_file.name

    # Docker configuration
    image_name = "codesavant-sandbox"
    container_path = f"/app/code{ext}"
    
    # Build command
    # docker run --rm --network none --memory 128m --cpus 0.5 -v host_path:container_path image_name command container_path
    
    docker_cmd = [
        'docker', 'run', '--rm',
        '--network', 'none',        # No internet access
        '--memory', '128m',         # Limit memory
        '--cpus', '0.5',            # Limit CPU
        '-v', f'{host_file_path}:{container_path}', # Mount file
        image_name
    ]
    
    # Add language specific command
    if isinstance(lang_config['cmd'], str):
        # Shell command (for compiled languages like C++)
        cmd_str = lang_config['cmd'].format(file=container_path)
        command = ['sh', '-c', cmd_str]
    else:
        # Direct command (for interpreted languages)
        command = lang_config['cmd'] + [container_path]
    
    # Special handling for compiled languages or complex commands could go here
    # For simplicity, we'll stick to interpreted languages for the MVP or simple run commands
    
    full_cmd = docker_cmd + command
    
    try:
        # Run the container
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=10 # 10 second timeout
        )
        
        output = result.stdout
        error = result.stderr
        
        # Clean up host file
        os.unlink(host_file_path)
        
        return output, error

    except subprocess.TimeoutExpired:
        os.unlink(host_file_path)
        return "", "Execution timed out (limit: 10s)."
    except Exception as e:
        if os.path.exists(host_file_path):
            os.unlink(host_file_path)
        return "", f"Sandbox error: {str(e)}"

def build_sandbox_image():
    """Helper to build the docker image if needed"""
    sandbox_dir = os.path.join(settings.BASE_DIR, 'sandbox')
    subprocess.run(['docker', 'build', '-t', 'codesavant-sandbox', sandbox_dir], check=True)
