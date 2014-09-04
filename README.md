# rpyle
### The Python Random Pile

Rpyle is a entropy gathering daemon able to access a multitude of entropy sources. Rpyle
then makes this entropy available via a webservice.


### Running rpyle

```
git clone https://github.com/zinic/rpyle.git
cd rpyle
pip install -r project/install_requires.txt
chmod +x src/scripts/rpyle

PYTHONPATH=src src/scripts/rpyle
```
