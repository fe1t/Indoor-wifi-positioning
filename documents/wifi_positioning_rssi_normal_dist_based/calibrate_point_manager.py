

from calibration import Calibration
import json
import pymysql.cursors
import pymysql



class CalibratePointManager():

    def __init__(self, config="config.json"):
        self.xy = []
        self.cpoints = []
        self.db = None
        with open(config, 'r') as f:
            self.config = json.load(f)

    def _get_db(self):
        return pymysql.connect(host=self.config['host'], user=self.config['user'], password=self.config['password'],  db=self.config['db'])

    def get_xy(self):
        self.db = self._get_db()
        with self.db.cursor() as cursor:
            sql = "select x, y from access_point group by x, y"
            cursor.execute(sql)
            rows = cursor.fetchall()
        return rows

    def get_cpoints(self):
        self.xy = self.get_xy()
        for (x, y) in self.xy:
            calibrate  = Calibration()
            cpoint = calibrate.get(x, y)
            self.cpoints.append(cpoint)
        return self.cpoints


obj = CalibratePointManager()
print len(obj.get_cpoints())
