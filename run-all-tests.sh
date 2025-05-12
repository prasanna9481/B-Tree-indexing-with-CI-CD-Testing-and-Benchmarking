py -3 driver.py test-data/small.txt py -3 sut.py

py -3 driver.py test-data/lookup.txt py -3 sut.py
py -3 driver.py test-data/lookup_big.txt py -3 sut.py

py -3 driver.py test-data/remove.txt py -3 sut.py
py -3 driver.py test-data/remove_big.txt py -3 sut.py

py -3 driver.py test-data/lowerbound.txt py -3 sut.py
py -3 driver.py test-data/lowerbound_big.txt py -3 sut.py
