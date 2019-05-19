part_manual = {
    "color": {
        "methods": {
            "GetColorName": {
                "arguments": [],
                "return": "string"
            }
        }
    },
    "ultrasonic": {
        "methods": {
            "GetDistance": {
                "arguments": [],
                "return": "int"
            }
        }
    },
    "controlSystem": {
        "methods": {
            "SetPower": {
                "arguments": [
                    {
                        "name": "left",
                        "type": "float"
                    },
                    {
                        "name": "right",
                        "type": "float"
                    }
                ],
                "return": None
            },
            "SetSpeed": {
                "arguments": [
                    {
                        "name": "left",
                        "type": "float"
                    },
                    {
                        "name": "right",
                        "type": "float"
                    }
                ],
                "return": None
            },
            "Brake": {
                "arguments": [
                    {
                        "name": "whichWheel",
                        "type": "string"
                    }
                ],
                "return": None
            }
        }
    },
    "gyro": {
        "methods": {
            "GetAngleX": {
                "arguments": [],
                "return": "float"
            },
            "GetAngleY": {
                "arguments": [],
                "return": "float"
            },
            "GetAngleZ": {
                "arguments": [],
                "return": "float"
            },
            "Reset": {
                "arguments": [],
                "return": None
            }
        }
    },
    "gps": {
        "methods": {

        }
    },
    "tl": {
        "methods": {
            "GetNearestTarget": {
                "arguments": [],
                "return": "vector3"
            }
        }
    },
    "grenadeLauncher": {
        "methods": {
            "Fire": {
                "arguments": [
                    {
                        "name": "force",
                        "type": "float"
                    }
                ],
                "return": None
            },
            "Rotate": {
                "arguments": [
                    {
                        "name": "right",
                        "type": "boolean"
                    }
                ],
                "return": None
            },
            "Lift": {
                "arguments": [
                    {
                        "name": "up",
                        "type": "boolean"
                    }
                ],
                "return": None
            },
            "GetCooldown": {
                "arguments": [],
                "return": "float"
            }
        }
    },
    "controller": {
        "methods": {
            "GetScore": {
                "arguments": [],
                "return": "float"
            }
        }
    }
}