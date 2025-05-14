import requests

class MeteoLugar:
    def __init__(self, long, lat):
        self.__longitud = long
        self.__latitud = lat


    def desplazarse(self, deltaLong, deltaLat):
        self.__longitud += deltaLong
        self.__latitud += deltaLat


    def getUrl(self):
        return (f'https://api.open-meteo.com/v1/forecast?'
                      f'latitude={self.__longitud}&longitude={self.__latitud}'
                      '&current_weather=true')

    def getWeather(self):
        respuesta= requests.get(self.getUrl())
        if respuesta.status_code != 200:
            print(f"Ha fallado con código {respuesta.status_code}")
        else:
            return respuesta.json()

    def temperatura(self):
        respuesta = self.getWeather()
        if respuesta:
            self.__temperaturaString(respuesta["current_weather"]["temperature"])
            return respuesta.get("current_weather").get("temperature")
        else:
            print(f"Json viene vacío, {respuesta}")

    def __temperaturaString(self, temp):
        respuesta=self.getWeather()
        print(f"La temperatura en {self.__longitud}, {self.__latitud} es {temp} {respuesta['current_weather_units']['temperature']}")




meteo = MeteoLugar(12,12)
meteo.temperatura()
meteo.desplazarse(0,-40)
meteo.temperatura()
