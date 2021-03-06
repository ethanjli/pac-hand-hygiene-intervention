"""Test script to control illumination from a MQTT topic."""

import argparse
import asyncio
import logging
import logging.config
import os

from intervention_system.deploy import (
    client_config_sample_cloudmqtt_name, client_configs_sample_path
)
from intervention_system.illumination.mqtt_client import Illuminator, topics
from intervention_system.mqtt_clients import message_string_encoding
from intervention_system.util import config
from intervention_system.util.async import (
    register_keyboard_interrupt_signals, run_function
)
from intervention_system.util.logging import logging_config

# Set up logging
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


class MockIlluminator(Illuminator):
    """Sets NeoPixel illumination based on messages from the broker."""

    def init_illumination(self):
        """Initialize illumination support."""
        pass

    def on_deployment_topic(self, client, userdata, msg):
        """Handle any device deployment messages."""
        command = msg.payload.decode(message_string_encoding)
        if command == 'reboot':
            logger.info('Mock rebooting (nop)...')
        elif command == 'shutdown':
            logger.info('Mock shutting down (nop)...')
        elif command == 'restart':
            logger.info('Mock restarting (nop)...')
        elif command == 'git pull':
            logger.info('Mock updating local repo (nop)...')
        elif command == 'stop':
            logger.info('Stopping...')
            raise KeyboardInterrupt

    def set_illumination(self, illumination_params):
        """Set the lights to some illumination."""
        logger.info('Mock setting lights to: {}'.format(illumination_params))

    async def attempt_reconnect(self):
        """Prepare the system for a reconnection attempt."""
        logger.info('Mock reconnecting (nop)...')
        await asyncio.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Receive illumination system messages.')
    parser.add_argument(
        '--config', '-c', type=str, default=client_config_sample_cloudmqtt_name,
        help=(
            'Name of client settings file in {}. Default: {}'
            .format(client_configs_sample_path, client_config_sample_cloudmqtt_name)
        )
    )
    args = parser.parse_args()
    config_name = args.config

    register_keyboard_interrupt_signals()

    # Load configuration
    config_path = os.path.join(client_configs_sample_path, config_name)
    configuration = config.config_load(config_path, keyfile_path=None)

    logger.info('Starting client...')
    loop = asyncio.get_event_loop()
    mqttc = MockIlluminator(loop, **configuration['broker'], topics=topics)
    run_function(mqttc.run)
    logger.info('Finished!')
