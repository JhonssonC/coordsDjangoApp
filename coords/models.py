import utm as utm
from django.db import models
import requests
import pyodbc



CRITERIOS = (
    ('Medidor', 'Medidor'),
    ('Código', 'Código')
)

class Cliente(models.Model):
    id = models.BigAutoField(primary_key=True)
    buscado_Criterio = models.CharField(
        max_length=20,
        choices=CRITERIOS,
        default='1'
    )
    servicio_sico = models.CharField(max_length=11)
    medidor_bpm = models.CharField(max_length=13)
    req_date = models.DateTimeField('Fecha de Requerimiento', auto_now=True)

    serie_bpm = models.CharField(max_length=13)
    medidor_sico = models.CharField(max_length=13)
    serie_sico = models.CharField(max_length=13)
    nombre_sico = models.CharField(max_length=50)
    geocod_sico = models.CharField(max_length=50)
    direccion_sico = models.CharField(max_length=50)
    agencia_sico = models.CharField(max_length=40)

    m_1 = models.CharField(max_length=13, default='')
    s_1 = models.CharField(max_length=13, default='')
    x_c1 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    y_c1 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    lat_c1 = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    lng_c1 = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    fecha1 = models.CharField(max_length=35)
    nove_1 = models.CharField(max_length=100)

    m_2 = models.CharField(max_length=13, default='')
    s_2 = models.CharField(max_length=13, default='')
    x_c2 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    y_c2 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    lat_c2 = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    lng_c2 = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    fecha2 = models.CharField(max_length=35)
    nove_2 = models.CharField(max_length=100)

    m_3 = models.CharField(max_length=13, default='')
    s_3 = models.CharField(max_length=13, default='')
    x_c3 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    y_c3 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    lat_c3 = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    lng_c3 = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    fecha3 = models.CharField(max_length=35)
    nove_3 = models.CharField(max_length=100)

    m_4 = models.CharField(max_length=13, default='')
    s_4 = models.CharField(max_length=13, default='')
    x_c4 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    y_c4 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    lat_c4 = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    lng_c4 = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    fecha4 = models.CharField(max_length=35)
    nove_4 = models.CharField(max_length=100)

    def request_a(self):

        CODIGO_PROVINCIA='110'

        if str(self.servicio_sico) == '':
            return

        codigocliente = str(self.servicio_sico)

        try:
            codigocliente = int(codigocliente)
        except(Exception):
            print(f'El valor de Codigo {self.servicio_sico} no puede ser considerado un valor valido para analisis.')
            return

        codigocliente = CODIGO_PROVINCIA + f"{codigocliente:07d}"
        # api-endpoint
        URL = f"https://amobile.altura.systems/abit/Ejecucion?n=CON_INF_LEC&wait=true&isJSON=true&criterioBusqueda=numero_servicio&numeroCuenta={codigocliente}"


        # sending get request and saving the response as response object
        r = requests.get(url=URL)

        # extracting data in json format
        data = r.json()

        #print(data)

        idResp = 1
        for r in data['data']['row']:
            if idResp > 4:
                break
            if r[9] == "SIN NOVEDAD":
                if idResp == 1:
                    self.medidor_bpm = str(r[18])
                    self.serie_bpm = str(r[19])

                    self.fecha1 = str(r[13])
                    self.nove_1 = str(r[9])
                    self.lat_c1 = str(r[11])
                    self.lng_c1 = str(r[12])
                    self.m_1 = str(r[18])
                    self.s_1 = str(r[19])

                if idResp == 2:
                    self.fecha2 = str(r[13])
                    self.nove_2 = str(r[9])
                    self.lat_c2 = str(r[11])
                    self.lng_c2 = str(r[12])
                    self.m_2 = str(r[18])
                    self.s_2 = str(r[19])

                if idResp == 3:
                    self.fecha3 = str(r[13])
                    self.nove_3 = str(r[9])
                    self.lat_c3 = str(r[11])
                    self.lng_c3 = str(r[12])
                    self.m_3 = str(r[18])
                    self.s_3 = str(r[19])

                if idResp == 4:
                    self.fecha4 = str(r[13])
                    self.nove_4 = str(r[9])
                    self.lat_c4 = str(r[11])
                    self.lng_c4 = str(r[12])
                    self.m_4 = str(r[18])
                    self.s_4 = str(r[19])

                self.xy_a(idr=idResp)

                idResp+=1





    def query_data(self):

        quer = ''
        if str(self.medidor_bpm) != '':
            quer = f"'{self.medidor_bpm}'"#query Medidor Search

        if str(self.servicio_sico) != '':
            quer = f"'{self.servicio_sico}'"#query Client Code Search

        data = {
            'kuery': quer,
            'un': 'MAN',
            'uid': '',#user of System
            'pwd': '',#password of System
        }
        try:
            conn = pyodbc.connect('')#string Connect to DSN for applies query
            cursor = conn.cursor()
            q = data['kuery']
            cursor.execute(q)

            headrs = []
            rows = cursor.description

            for row in rows:
                headrs.append(row[0])


            all = []

            rows = cursor.fetchall()
            for row in rows:
                all.append([x for x in row])

            for i in range(len(all)):
                for j in range(len(all[i])):
                    if isinstance(all[i][j], str):
                        all[i][j] = (all[i][j]).strip()

            cursor.close()
            conn.close()

            res = [headrs, all]

            print(res)

            # mapping
            self.servicio_sico = all[0][0]
            self.nombre_sico = all[0][1]
            self.direccion_sico = all[0][2]
            self.agencia_sico = all[0][3]
            self.geocod_sico = all[0][4]
            self.medidor_sico = all[0][5]
            self.serie_sico = all[0][6]
            self.marca_sico = all[0][7]

        except (Exception):
            self.nombre_sico = "Error Cliente no encontrado..."
            print("Error al ejecutar Busqueda...")



    def xy_a(self, idr=1):
        lat = 0
        lng = 0
        match idr:
            case 1:
                lat = str(self.lat_c1)
                lng = str(self.lng_c1)
            case 2:
                lat = str(self.lat_c2)
                lng = str(self.lng_c2)

            case 3:
                lat = str(self.lat_c3)
                lng = str(self.lng_c3)

            case 4:
                lat = str(self.lat_c4)
                lng = str(self.lng_c4)

        # api-endpoint ArcGis onlineApi for transform coords
        URL = f"https://utility.arcgisonline.com/arcgis/rest/services/Geometry/GeometryServer/project?f=json&outSR=32717&inSR=4326&geometries=%7B%22geometryType%22%3A%22esriGeometryPoint%22%2C%22geometries%22%3A%5B%7B%22x%22%3A" +lng+ "%2C%22y%22%3A" +lat+ "%2C%22spatialReference%22%3A%7B%22wkid%22%3A4326%2C%22latestWkid%22%3A4326%7D%7D%5D%7D"

        # sending get request and saving the response as response object
        r = requests.get(url=URL)

        # extracting data in json format
        data = r.json()

        print(data)
        try:
            match idr:
                case 1:
                    self.x_c1 = data['geometries'][0]['x']
                    self.y_c1 = data['geometries'][0]['y']
                case 2:
                    self.x_c2 = data['geometries'][0]['x']
                    self.y_c2 = data['geometries'][0]['y']
                case 3:
                    self.x_c3 = data['geometries'][0]['x']
                    self.y_c3 = data['geometries'][0]['y']
                case 4:
                    self.x_c4 = data['geometries'][0]['x']
                    self.y_c4 = data['geometries'][0]['y']
        except (Exception):
            pass




    def xy_b(self, idr=1):
        try:

            match idr:
                case 1:
                    lat = str(self.lat_c1)
                    lng = str(self.lng_c1)
                case 2:
                    lat = str(self.lat_c2)
                    lng = str(self.lng_c2)
                case 3:
                    lat = str(self.lat_c3)
                    lng = str(self.lng_c3)
                case 4:
                    lat = str(self.lat_c4)
                    lng = str(self.lng_c4)

            x, y, zone, ut = utm.from_latlon(lat, lng, force_zone_letter='S')

            match idr:
                case 1:
                    self.x_c1 = x
                    self.y_c1 = y
                case 2:
                    self.x_c2 = x
                    self.y_c2 = y
                case 3:
                    self.x_c3 = x
                    self.y_c3 = y
                case 4:
                    self.x_c4 = x
                    self.y_c4 = y
        except (Exception):
            pass