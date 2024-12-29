# CryptoBot

<details>
<summary>setup vm</summary>

## add new repository in git browser

git clone https://github.com/scaja/CryptoBot.git  
cd CryptoBot  
git add .gitignore  
git commit -m "add gitignore"  
git push  
source myenv/bin/activatesource  


## virtual environment

sudo apt-get update  
sudo apt-get install python3.8-venv --fix-missing  
python3 -m venv myenv  
source myenv/bin/activate  


upgrade pip  
python3 -m pip install --upgrade pip  


## Create Kernel

pip3 install ipykernel  
python3 -m ipykernel install --user --name='vscode'  


## Start Jupiter

pip install notebook ipython  
jupyter notebook  
Install extensions also as host ssh  
restart VSCODE manuelly  

</details>

<details>
<summary>install packages</summary>

pip install pandas  
pip install python-dotenv  
pip install python-binance  
pip install websocket-client
pip install elasticsearch

</details>

<details>
<summary>unittest</summary>

python -m unittest discover

</details>

