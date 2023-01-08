
    var worker = cw({
        init: function(scope) {
            //importScripts('/static/js/coordenadas/require.js');
            require.config({
                baseUrl: this.base
            });
            require(['shp'], function(shp) {
                scope.shp = shp;
            });
        },
        data: function(data, cb, scope) {
            this.shp(data).then(function(geoJson){
                if(Array.isArray(geoJson)){
                    geoJson.forEach(function(geo){
                        scope.json([geo, geo.fileName, true],true,scope);
                    });
                }else{
                    scope.json([geoJson, geoJson.fileName, true],true,scope);
                }
            }, function(e) {
                console.log('shit', e);
            });

        },
        color:function(s){
            //from http://stackoverflow.com/a/15710692
            importScripts('/static/js/coordenadas/colorbrewer.js');
            return colorbrewer.Spectral[11][Math.abs(JSON.stringify(s).split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0)) % 11];
        },
        makeString:function(buffer) {
                var array = new Uint8Array(buffer);
                var len = array.length;
                var outString = "";
                var i = 0;
                while (i < len) {
                    outString += String.fromCharCode(array[i++]);
                }
                return outString;
            },
        json: function(data, cb, scope) {
            importScripts('/static/js/coordenadas/topojson.v1.min.js');
            var name = data[1];
            //console.log(name);
            var json = data.length === 2 ? JSON.parse(scope.makeString(data[0])) : data[0];
            var nom;
            if (json.type === 'Topology') {
                for (nom in json.objects) {
                    scope.layer(topojson.feature(json, json.objects[nom]), nom, scope);
                }
            }
            else {
                scope.layer(json, name, scope);
            }
        },layer:function(json,name,scope){
            
            json.features.forEach(function(feature){
                feature.properties.__color__ = scope.color(feature);
            });
            scope.fire('json',[json,name]);
        },
        base: cw.makeUrl('.')
    });
    function readerLoad() {
        if (this.readyState !== 2 || this.error) {
            return;
        }
        else {
            worker.data(this.result, [this.result]);
        }
    }

    function handleZipFile(file) {
        
        var reader = new FileReader();
        reader.onload = readerLoad;
        reader.readAsArrayBuffer(file);
    }

    function handleFile(file) {

        m.spin(true);
        if (file.name.slice(-3) === 'zip') {
            return handleZipFile(file);
        }
        var reader = new FileReader();
        reader.onload = function() {
            var ext;
            if (reader.readyState !== 2 || reader.error) {
                return;
            }
            else {
                ext = file.name.split('.');
                ext = ext[ext.length - 1];


                worker.json([reader.result, file.name.slice(0, (0 - (ext.length + 1)))], [reader.result]);
            }
        };
        reader.readAsArrayBuffer(file);
    }


    var url = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'

    var optionsObject ={
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }

    var mq = L.tileLayer(url, optionsObject);
    var watercolor = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    })
    mq.addTo(m);
    var lc = L.control.layers({
        "Stamen Watercolor": watercolor,
        "Stamen Toner": mq
    }).addTo(m);
    //make the map
    var options = {
        onEachFeature: function(feature, layer) {
            if (feature.properties) {
                layer.bindPopup(Object.keys(feature.properties).map(function(k) {
                    if(k === '__color__'){
                        return;
                    }
                    return k + ": " + feature.properties[k];
                }).join("<br />"), {
                    maxHeight: 200
                });
            }
        },
        style: function(feature) {
            return {
                opacity: 1,
                fillOpacity: 0.7,
                radius: 6,
                color: feature.properties.__color__
            }
        },
        pointToLayer: function(feature, latlng) {
            return L.circleMarker(latlng, {
                opacity: 1,
                fillOpacity: 0.7,
                color: feature.properties.__color__
            });
        }
    };




    function setWorkerEvents() {
        worker.on('json', function(e) {
            //m.spin(false);
            lc.addOverlay(L.geoJson(e[0], options).addTo(m), e[1]);
        });
        worker.on('error', function(e) {
            console.warn(e);
        });
    }

//setWorkerEvents();




