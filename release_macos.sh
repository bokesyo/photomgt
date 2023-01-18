rm -rf ./dist/
pyi-makespec -D manage.py
pyinstaller manage.spec
cp -r data templates ./dist/manage/
rm -rf ./dist/manage/data/*.json
rm -rf manage.spec 
rm -rf ./build/
cp -r ./test_data ./dist/
zip -r release_macos.zip ./dist/

