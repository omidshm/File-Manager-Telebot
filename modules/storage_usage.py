import psutil
from dataclasses import dataclass

@dataclass
class DriveUsage:
    drive: str
    total_gb: float
    used_gb: float
    free_gb: float
    percent_used: float
    
    def __repr__(self) -> str:
        return f"Drive: {self.drive}\nTotal: {round(self.total_gb, 2)}Gb\nUsed: {self.percent_used}%"

def get_drive_usage(drive_letter: str = 'C:/') -> DriveUsage:
    # Get the disk usage statistics for the specified drive
    usage = psutil.disk_usage(drive_letter)
    
    # Create an instance of DriveUsage dataclass
    drive_usage = DriveUsage(
        drive=drive_letter,
        total_gb=usage.total / (1024 ** 3),
        used_gb=usage.used / (1024 ** 3),
        free_gb=usage.free / (1024 ** 3),
        percent_used=usage.percent
    )
    
    return drive_usage