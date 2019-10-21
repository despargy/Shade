#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Sun Oct 20 19:07:57 2019
##################################################


from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fec
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import limesdr


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################


        self.variable_cc_encoder_def_0 = variable_cc_encoder_def_0 = map( (lambda a: fec.cc_encoder_make(4096, 7, 2, ([79,109]), 0, fec.CC_STREAMING, False)), range(0,1) );


        self.variable_cc_decoder_def_0 = variable_cc_decoder_def_0 = map( (lambda a: fec.cc_decoder.make(4096, 7, 2, ([79,109]), 0, -1, fec.CC_STREAMING, False)), range(0,1) );
        self.samp_rate = samp_rate = 50000
        self.code1 = code1 = '010110011011101100010101011111101001001110001011010001101010001'

        ##################################################
        # Blocks
        ##################################################
        self.limesdr_sink_0 = limesdr.sink('1D4984C0B2BBE9', 0, '', '')
        self.limesdr_sink_0.set_sample_rate(samp_rate)
        self.limesdr_sink_0.set_center_freq(1.43e9, 0)
        self.limesdr_sink_0.set_bandwidth(5e6,0)
        self.limesdr_sink_0.set_digital_filter(samp_rate,0)
        self.limesdr_sink_0.set_gain(60,0)
        self.limesdr_sink_0.set_antenna(255,0)

        self.digital_gmsk_mod_0 = digital.gmsk_mod(
        	samples_per_symbol=2,
        	bt=0.35,
        	verbose=False,
        	log=False,
        )
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, 32000,True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/pi/Desktop/Despar/Shade/spon.jpg', False)
        self.blks2_packet_encoder_0_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=4,
        		bits_per_symbol=1,
        		preamble='',
        		access_code=code1,
        		pad_for_usrp=False,
        	),
        	payload_length=0,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_packet_encoder_0_0, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blks2_packet_encoder_0_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.limesdr_sink_0, 0))

    def get_variable_cc_encoder_def_0(self):
        return self.variable_cc_encoder_def_0

    def set_variable_cc_encoder_def_0(self, variable_cc_encoder_def_0):
        self.variable_cc_encoder_def_0 = variable_cc_encoder_def_0

    def get_variable_cc_decoder_def_0(self):
        return self.variable_cc_decoder_def_0

    def set_variable_cc_decoder_def_0(self, variable_cc_decoder_def_0):
        self.variable_cc_decoder_def_0 = variable_cc_decoder_def_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.limesdr_sink_0.set_digital_filter(self.samp_rate,0)

    def get_code1(self):
        return self.code1

    def set_code1(self, code1):
        self.code1 = code1


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()