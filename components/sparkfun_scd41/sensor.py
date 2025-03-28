import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import (
    CONF_ID,
    CONF_UPDATE_INTERVAL,
    UNIT_PARTS_PER_MILLION,
    UNIT_CELSIUS,
    UNIT_PERCENT,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_HUMIDITY,
    STATE_CLASS_MEASUREMENT,
    ICON_MOLECULE_CO2,
    ICON_THERMOMETER,
    ICON_WATER_PERCENT,
)
from esphome.components import sensor, i2c

DEPENDENCIES = ["i2c"]
AUTO_LOAD = ["sensor"]

sparkfun_scd41_ns = cg.esphome_ns.namespace("sparkfun_scd41")
# This name must match your C++ class in sparkfun_scd41.h:
SCD41Component = sparkfun_scd41_ns.class_(
    "SCD41Component",  # Matches the .h/.cpp
    cg.PollingComponent,
    i2c.I2CDevice,
)

CONF_CO2 = "co2"
CONF_TEMPERATURE = "temperature"
CONF_HUMIDITY = "humidity"

CONFIG_SCHEMA = cv.All(
    sensor.sensor_schema(SCD41Component).extend({
        cv.Optional(CONF_CO2): sensor.sensor_schema(
            unit_of_measurement=UNIT_PARTS_PER_MILLION,
            icon=ICON_MOLECULE_CO2,
            accuracy_decimals=1,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            icon=ICON_THERMOMETER,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_HUMIDITY): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            icon=ICON_WATER_PERCENT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_HUMIDITY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    })
    .extend(i2c.i2c_device_schema(0x62))
    .extend({
        cv.Optional(CONF_UPDATE_INTERVAL, default="60s"): cv.update_interval,
    })
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL]))

    if CONF_CO2 in config:
        co2_sensor = await sensor.new_sensor(config[CONF_CO2])
        cg.add(var.set_co2_sensor(co2_sensor))

    if CONF_TEMPERATURE in config:
        temperature_sensor = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature_sensor(temperature_sensor))

    if CONF_HUMIDITY in config:
        humidity_sensor = await sensor.new_sensor(config[CONF_HUMIDITY])
        cg.add(var.set_humidity_sensor(humidity_sensor))
