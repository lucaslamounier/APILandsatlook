# APILandsatlook

ApiLandsatlook api to get data from usgs landsatlook

Installation
------------

    $ git clone https://github.com/lucaslamounier/APILandsatlook.git
    
    $ cd APILandsatlook
    
    $ python setup.py install 

Usage
-----
    api = ApiLandsatlook()
    api.query(start_date='2015-01-01', end_date='2016-12-31', cloudCover='40', xmin='-6366732.060713638',
              ymin='-377242.91314659826', xmax='-5877535.079688745', ymax='-137230.64433126024')
    products = api.get_products()
    bbox = [-6366732.060713638, -377242.91314659826, -5877535.079688745, -137230.64433126024]
    png_url = api.get_processed_image_png(bbox=bbox, contrast='stretch')
    
License
=======

Copyright © Lucas Lamounier.

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    
