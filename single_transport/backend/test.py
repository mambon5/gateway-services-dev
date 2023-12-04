import unittest

import global_vars as gvar
import otap_specific_functions as ospef

class TestGetWNI(unittest.TestCase):
    
    def test_get_wni(self):
        wni = gvar.create_wni()
        gws = list(wni.get_gateways())
        print(" gateway list: {}".format(gws))
        self.assertIsNot(gws, [])

    def test_sink_id(self):
        wni = gvar.create_wni()
        [sink, gw_id] = gvar.get_sink_and_gw(wni)
        print(" sink: {}".format(sink))
        self.assertIsNot(sink, None)

    def test_gw_id(self):
        wni = gvar.create_wni()
        [sink, gw_id] = gvar.get_sink_and_gw(wni)
        self.assertIsNot(gw_id, None)

    def test_get_otapHelper(self):
        wni = gvar.create_wni()
        print("otap helper")
        self.assertIsNot(gvar.create_otaphelper(wni), None)

    def test_get_node_list(self):
        wni = gvar.create_wni()
        otapHelper = gvar.create_otaphelper(wni)
        self.assertIsNot(ospef.get_node_list(otapHelper), None)


if __name__ == '__main__':
    unittest.main()
