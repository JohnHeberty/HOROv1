def LatLon_to_GrauMinute(latitude, longitude):
    
    def decimal_para_dms(coordenada):
        graus = int(coordenada)
        minutos_flutuantes = (coordenada - graus) * 60
        minutos = int(minutos_flutuantes)
        segundos = round((minutos_flutuantes - minutos) * 60, 0)
        return graus, minutos, segundos
    
    lat_dir = 'N' if latitude >= 0 else 'S'
    lon_dir = 'E' if longitude >= 0 else 'W'
    lat_dms = decimal_para_dms(abs(latitude))
    lon_dms = decimal_para_dms(abs(longitude))
    LatEnd = f"{lat_dms[0]}°{lat_dms[1]}`{lat_dms[1]}``{lat_dir}"
    LonEnd = f"{lon_dms[0]}°{lon_dms[1]}`{lon_dms[1]}``{lon_dir}"
    return LatEnd, LonEnd