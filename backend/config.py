#!/usr/bin/env python3
"""App configuration."""


class Config:
    """Configuration settings."""
    SECRET_KEY = "makesomenoise"
    DATABASE_NAME = "noisemakers_db"
    MONGODB_URI = f"mongodb://localhost:27017/{DATABASE_NAME}"
