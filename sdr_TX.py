#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Aug 30 18:06:51 2019
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fec
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import limesdr
import sip
import sys
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################


        self.variable_cc_encoder_def_0 = variable_cc_encoder_def_0 = map( (lambda a: fec.cc_encoder_make(4096, 7, 2, ([79,109]), 0, fec.CC_STREAMING, False)), range(0,1) );


        self.variable_cc_decoder_def_0 = variable_cc_decoder_def_0 = map( (lambda a: fec.cc_decoder.make(4096, 7, 2, ([79,109]), 0, -1, fec.CC_STREAMING, False)), range(0,1) );
        self.samp_rate = samp_rate = 500000
        self.code1 = code1 = '010110011011101100010101011111101001001110001011010001101010001'

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
        	1024, #size
        	samp_rate, #samp_rate
        	"Transmission", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.limesdr_sink_0 = limesdr.sink('1D4984C0B2BBE9', 0, '', '')
        self.limesdr_sink_0.set_sample_rate(samp_rate)
        self.limesdr_sink_0.set_center_freq(433e6, 0)
        self.limesdr_sink_0.set_bandwidth(5e6,0)
        self.limesdr_sink_0.set_digital_filter(500e3,0)
        self.limesdr_sink_0.set_gain(20,0)
        self.limesdr_sink_0.set_antenna(255,0)

        self.digital_gmsk_mod_0 = digital.gmsk_mod(
        	samples_per_symbol=2,
        	bt=0.35,
        	verbose=False,
        	log=False,
        )
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, 32000,True)
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (264/8, 1650304/8))
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, '/home/beam/Desktop/in2.txt', True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/beam/Desktop/SHADE/GnuRadio/in.txt', True)
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
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blks2_packet_encoder_0_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.limesdr_sink_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.qtgui_time_sink_x_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

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
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)

    def get_code1(self):
        return self.code1

    def set_code1(self, code1):
        self.code1 = code1


def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
