"""Fixture aislado: ejecuta HarmocapPipeline.step real con objetos sintéticos.

Uso: python3 research/verificar_harmocap_bands_osc.py /ruta/a/HarMoCAP
El checkout debe estar en 25fda8d74c663a573aab6bc8f540c2c46ef250b9.
No inicia cámara, backend, socket ni servicio. Ejecuta el método de ese checkout.
"""
import ast
import importlib.util
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

if len(sys.argv) != 2:
    raise SystemExit(__doc__)
root = Path(sys.argv[1])
pin = '25fda8d74c663a573aab6bc8f540c2c46ef250b9'
head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
if head != pin:
    raise SystemExit(f'HarMoCAP debe estar en {pin}; encontrado: {head}')
dirty = subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True)
if dirty:
    raise SystemExit('El checkout de HarMoCAP debe estar limpio')
source = root / 'src/harmocap/pipeline.py'
codec_source = root / 'src/harmocap/interface/osc_codec.py'
spec = importlib.util.spec_from_file_location('actual_osc_codec', codec_source)
codec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(codec)
tree = ast.parse(source.read_text())
cls = next(x for x in tree.body if isinstance(x, ast.ClassDef) and x.name == 'HarmocapPipeline')
method = next(x for x in cls.body if isinstance(x, ast.FunctionDef) and x.name == 'step')
namespace = {
    'KeypointData': lambda **kw: SimpleNamespace(**kw),
    'PersonState': lambda **kw: SimpleNamespace(**kw),
    'MovementFrame': lambda **kw: SimpleNamespace(**kw),
    'osc_codec': codec,
    'mono_us': lambda: 1_001_000,
}
exec(compile(ast.Module(body=[method], type_ignores=[]), str(source), 'exec'), namespace)
step = namespace['step']

points = [(0.6, 0.4, .99, 0, 0, 0) for _ in range(17)]
points[5] = (.5, .4, .99, 0, 0, 0)
points[6] = (.7, .4, .99, 0, 0, 0)
points[9] = (.2, .5, .99, 0, 0, 0)
points[10] = (1.0, .5, .99, 0, 0, 0)
class FakeFeatures:
    def _torso_height(self, *args): return 1.0
    def extract(self, *args): return ([0.] * 24, [0] * 24)
class FakeEmitter:
    def __init__(self): self.wire = None
    def emit(self, frame, wire, **kwargs): self.wire = wire; return []
class Fake:
    def _slot_state(self, *args):
        return (SimpleNamespace(update=lambda *args: tuple(points)), FakeFeatures())

def run(bands):
    fake = Fake()
    fake.camera = SimpleNamespace(get_latest=lambda: ('synthetic',1,1_000_000), profile=lambda: {'fps':30.})
    fake.backend = SimpleNamespace(track_frame=lambda frame: ([],[],0,(1280,720)))
    detection = SimpleNamespace(bbox_xywhn=(.5,.5,.3,.5), keypoints_iso=[p[:3] for p in points])
    event = SimpleNamespace(detection=detection,slot_id=0,slot_reset=False,emit_tombstone=False)
    fake.slots = SimpleNamespace(update=lambda *args,**kwargs:[event], focused_slot=0)
    fake.crowd = SimpleNamespace(update=lambda *args,**kwargs:{})
    fake.density = None
    fake.raw_keypoints = False
    fake.calib = SimpleNamespace(observe=lambda *args: False, profile=SimpleNamespace(state='frozen',generation=1))
    fake._band_span = {}
    fake._bands_mode = bands
    fake.metrics = {'frames':0,'emitted':0,'lat_sw_ms':[],'jitter_ms':[]}
    fake.emitter = FakeEmitter()
    fake.recorder = None
    fake.stream_id = 'synthetic'
    assert step(fake)
    blob = fake.emitter.wire[0]['keypoints_blob']
    kps = codec.unpack_keypoints(blob)
    return (kps[9][0],kps[10][0]), (fake.last_persons[0].raw_keypoints[9].x, fake.last_persons[0].raw_keypoints[10].x)

grid, raw_grid = run(False)
bands, raw_bands = run(True)
assert all(abs(a-b)<1e-6 for a,b in zip(grid,(.2,1.0))), grid
assert all(abs(a-.8)<1e-6 for a in bands), bands
assert raw_grid == raw_bands == (.2,1.0)
print('grid OSC wrist x:',grid)
print('bands OSC wrist x:',bands)
print('both local raw wrist x:',raw_bands)
