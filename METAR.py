# written by the gitHub ai, not me, I'm just testing things and seeing how well it works

import re
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class METAR:
    """METAR weather report data"""
    station: str
    time: str
    wind_direction: Optional[int] = None
    wind_speed: Optional[int] = None
    wind_gust: Optional[int] = None
    visibility: Optional[str] = None
    weather: List[str] = None
    temperature: Optional[float] = None
    dew_point: Optional[float] = None
    altimeter: Optional[float] = None

    def __post_init__(self):
        if self.weather is None:
            self.weather = []

def parse_metar(metar_string: str) -> METAR:
    """Parse a METAR string and extract weather information"""
    parts = metar_string.strip().split()
    
    if not parts:
        raise ValueError("Empty METAR string")
    
    station = parts[0]
    time = parts[1] if len(parts) > 1 else ""
    
    metar = METAR(station=station, time=time)
    
    i = 2
    while i < len(parts):
        part = parts[i]
        
        # Wind direction and speed (e.g., 18010KT)
        if re.match(r'^\d{3}\d{2}(KT|MPS|G\d{2}KT)?$', part):
            try:
                metar.wind_direction = int(part[:3])
                metar.wind_speed = int(part[3:5])
                if 'G' in part:
                    gust_match = re.search(r'G(\d{2})', part)
                    if gust_match:
                        metar.wind_gust = int(gust_match.group(1))
            except ValueError:
                pass
        
        # Visibility (e.g., 10SM, 9999, 1200V1600)
        elif re.match(r'^\d+(SM|V\d+)?$', part) or 'SM' in part:
            metar.visibility = part
        
        # Temperature and dew point (e.g., 15/10)
        elif re.match(r'^(M?\d{2})/(M?\d{2})$', part):
            try:
                temp_str = part.split('/')[0].replace('M', '-')
                dew_str = part.split('/')[1].replace('M', '-')
                metar.temperature = float(temp_str)
                metar.dew_point = float(dew_str)
            except ValueError:
                pass
        
        # Altimeter (e.g., A3012, Q1015)
        elif re.match(r'^(A|Q)\d{4}$', part):
            try:
                metar.altimeter = float(part[1:]) / 100
            except ValueError:
                pass
        
        # Weather phenomena (e.g., RA, SN, -RA)
        elif re.match(r'^(-|\+)?(VC)?(RA|SN|DZ|PL|SG|IC|PE|GR|GS|UP)$', part):
            metar.weather.append(part)
        
        i += 1
    
    return metar

def print_metar(metar: METAR) -> None:
    """Print METAR information in readable format"""
    print(f"Station: {metar.station}")
    print(f"Time: {metar.time}")
    if metar.wind_direction is not None:
        print(f"Wind: {metar.wind_direction}° at {metar.wind_speed} kt", end="")
        if metar.wind_gust:
            print(f" gusting {metar.wind_gust} kt")
        else:
            print()
    if metar.visibility:
        print(f"Visibility: {metar.visibility}")
    if metar.temperature is not None:
        print(f"Temperature: {metar.temperature}°C")
    if metar.dew_point is not None:
        print(f"Dew point: {metar.dew_point}°C")
    if metar.altimeter is not None:
        print(f"Altimeter: {metar.altimeter} inHg")
    if metar.weather:
        print(f"Weather: {', '.join(metar.weather)}")

if __name__ == "__main__":
    example_metar = "KCOS 090354Z 33006KT 10SM FEW100 BKN180 BKN250 20/10 A3010 RMK AO2 SLP103 T01940100"
    metar_data = parse_metar(example_metar)
    print_metar(metar_data)
