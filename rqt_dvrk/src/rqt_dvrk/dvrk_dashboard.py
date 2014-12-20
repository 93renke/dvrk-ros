# Zihan Chen
# 2014-12-19


from qt_gui.plugin import Plugin
from python_qt_binding import QtGui
from python_qt_binding import QtCore
from python_qt_binding.Qwt.Qwt import QwtThermo


# TODO
#  - set robot to bold
#  - subscribe to joint states

class dvrkDashboard(Plugin):
    def __init__(self, context):
        super(dvrkDashboard, self).__init__(context)

        # give QObjects reasonable names
        self.setObjectName('dvrkDashboard')

        # process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                            dest="quiet",
                            help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print 'arguments: ', args
            print 'unknowns: ', unknowns

        # create qwidget
        self._widget = QtGui.QWidget()
        self._widget.setObjectName('dvrkDashboardUI')

        # serial number
        if context.serial_number() > 1:
            self._widget.setWindowTitle(
                self._widget.windowTitle() + (' (%d)' % context.serial_number()))

        # add widget to the user interface
        context.add_widget(self._widget)
        self.context = context

        # ---- Get Widget -----
        self.init_ui()
        pass

    def init_ui(self):
        # type combobox
        ui_type_lable = QtGui.QLabel('Robot')
        ui_type_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.ui_type = QtGui.QComboBox()
        self.ui_type.addItem('MTMR')
        self.ui_type.addItem('MTML')
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(ui_type_lable)
        hbox.addWidget(self.ui_type)

        # control mode
        # todo: use a for loop
        gbox = QtGui.QGridLayout()
        ui_btn_idle = QtGui.QPushButton('Idle')
        gbox.addWidget(ui_btn_idle, 0, 0)
        ui_btn_idle.clicked[bool].connect(self.cb_btn_idle)

        ui_btn_home = QtGui.QPushButton('Home')
        gbox.addWidget(ui_btn_home, 0, 1)
        ui_btn_home.clicked[bool].connect(self.cb_btn_home)

        ui_btn_grav = QtGui.QPushButton('Gravity')
        gbox.addWidget(ui_btn_grav, 1, 0)
        ui_btn_grav.clicked[bool].connect(self.cb_btn_grav)

        ui_btn_vfix = QtGui.QPushButton('Virtual Fixture')
        gbox.addWidget(ui_btn_vfix, 1, 1)
        ui_btn_vfix.clicked[bool].connect(self.cb_btn_vfix)

        # connect here
        ui_gbox_control = QtGui.QGroupBox('Control')
        ui_gbox_control.setLayout(gbox)

        # joint position group
        jnt_pos_hbox = QtGui.QHBoxLayout()
        for i in range(7):
            pos_vbox = QtGui.QVBoxLayout()
            ui_ppos = QwtThermo()
            ui_ppos.setScalePosition(QwtThermo.NoScale)
            ui_ppos.setAutoFillBackground(True)
            ui_ppos.setAlarmLevel(0.8)
            ui_ppos.setPipeWidth(20)
            ui_ppos.setValue(0.9)
            ui_ppos.setMinimumSize(0, 30)
            ui_npos = QwtThermo()
            ui_npos.setScalePosition(QwtThermo.NoScale)
            ui_npos.setAlarmLevel(0.8)
            ui_npos.setPipeWidth(20)
            ui_npos.setValue(0.9)
            ui_npos.setMinimumSize(0, 30)
            ui_label_jnt = QtGui.QLabel('J' + str(i))
            pos_vbox.addWidget(ui_ppos)
            pos_vbox.addWidget(ui_npos)
            pos_vbox.addWidget(ui_label_jnt)
            jnt_pos_hbox.addLayout(pos_vbox)
            print i

        # ui_btn_jnt_pos = QPushButton('J1')
        ui_gbox_jnt_pos = QtGui.QGroupBox('Joint Positions (normalized)')
        ui_gbox_jnt_pos.setLayout(jnt_pos_hbox)

        # joint torque group

        # main layout
        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(hbox)
        main_layout.addWidget(ui_gbox_control)
        main_layout.addWidget(ui_gbox_jnt_pos)
        self._widget.setLayout(main_layout)
        pass

    def shutdown_plugin(self):
        # del publishers
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO: save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    def cb_btn_home(self, checked):
        print 'home btn pressed'
        pass

    def cb_btn_idle(self, checked):
        print 'idle btn pressed'
        pass

    def cb_btn_grav(self, checked):
        print 'grav btn pressed'
        pass

    def cb_btn_vfix(self, checked):
        print 'vfix btn pressed'
        pass
