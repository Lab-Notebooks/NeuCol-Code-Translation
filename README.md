## Laboratory Notebook for LLM-Based Code Engineering for Scientific Computing Applications

Code Llama Paper: https://arxiv.org/abs/2308.12950

Request License: https://ai.meta.com/resources/models-and-libraries/llama-downloads/

### Setting up Code Llama

1. Create a site specific file for your cuda environments. See existing site configurations.
2. `pip3 install -r requirements.txt`. This will install `jobrunner`
3. `./configure -s <site-name>`
4. Make sure `jobrunner` is in your path.
5. `jobrunner setup software/codellama -V`
6. `jobrunner setup models/codellama -V`. Follow instructions to provide license url and download desired models (7b,7b-Instruct,etc...)
8.  Edit `Jobfile` in project root directory to set appropriate schedular commands. 
9. `jobrunner submit runs/Example/completions -V`
10. `jobrunner submit runs/Example/instructions -V`

### Hugging face
1. huggingface-cli login --token <huggingface-token>
