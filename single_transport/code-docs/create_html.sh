rm -r source/modules/*.rst
rm -r build
mkdir build
sphinx-apidoc -o source/modules/ ../backend/
./create_index_rst.sh
mv index.rst source/
make html
firefox build/html/index.html


