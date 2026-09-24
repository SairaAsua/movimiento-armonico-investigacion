"""Pérdida de información en dos mapeos pitch-espacio sobre un icosaedro ideal.

No es fórmula de Laban ni estudio perceptivo. Usa la secuencia de White 2020.
"""

from collections import Counter
from itertools import combinations

from simetrias_laban import PHI, d2


POINTS = {
    1: (0, 1, PHI), 2: (0, -1, PHI),
    3: (PHI, 0, 1), 4: (-PHI, 0, 1),
    5: (1, PHI, 0), 6: (-1, PHI, 0),
    7: (1, -PHI, 0), 8: (-1, -PHI, 0),
    9: (0, 1, -PHI), 10: (0, -1, -PHI),
    11: (PHI, 0, -1), 12: (-PHI, 0, -1),
}
WHITE_ORDER = (1, 3, 5, 9, 11, 7, 10, 12, 8, 2, 4, 6)


def main():
    edges = {frozenset((a, b)) for a, b in combinations(POINTS, 2)
             if abs(d2(POINTS[a], POINTS[b]) - 4) < 1e-9}
    assert len(edges) == 30
    degree = Counter(v for edge in edges for v in edge)
    assert set(degree.values()) == {5}

    # Asignar 12 clases de altura a la ruta de White, índice cromático 0..11.
    pitch = {v: i for i, v in enumerate(WHITE_ORDER)}
    semitone_neighbors = {frozenset((WHITE_ORDER[i], WHITE_ORDER[(i + 1) % 12]))
                          for i in range(12)}
    assert semitone_neighbors <= edges and len(semitone_neighbors) == 12
    by_interval = Counter(min(abs(pitch[a] - pitch[b]), 12 - abs(pitch[a] - pitch[b]))
                          for a, b in (tuple(edge) for edge in edges))
    assert sum(by_interval.values()) == 30
    assert by_interval[1] == 12
    print('icosaedro: vertices=12 aristas=30 grado=5; '
          'pitch_cromatico: clases=12 vecinos_semitono=12 grado=2')
    print('ruta_White: aristas_que_suenan_como_semitono=12/30; '
          f'aristas_con_intervalo_mayor=18/30; histograma_intervalos={dict(sorted(by_interval.items()))}')

    # Cualquier biyección vértice→clase cromática tiene sólo 12 pares a distancia
    # de semitono en el ciclo; no puede preservar las 30 adyacencias como tales.
    assert len(semitone_neighbors) < len(edges)

    # Mapear sólo altura vertical colapsa vértices aun con medida exacta.
    heights = Counter(round(p[2], 9) for p in POINTS.values())
    assert len(heights) == 5 and sorted(heights.values()) == [2, 2, 2, 2, 4]
    print(f'altura_sola: 12_vertices_a_{len(heights)}_niveles; '
          f'multiplicidades={sorted(heights.values())}')

    # Dos líneas paralelas tienen idéntico vector de orientación, distinta
    # situación respecto del centro corporal; pitch(direction) las fusiona.
    central_start, central_end = (-0.5, 0, 0), (0.5, 0, 0)
    peripheral_start, peripheral_end = (-0.5, 1, 0), (0.5, 1, 0)
    central_vector = tuple(b - a for a, b in zip(central_start, central_end))
    peripheral_vector = tuple(b - a for a, b in zip(peripheral_start, peripheral_end))
    assert central_vector == peripheral_vector == (1, 0, 0)
    assert central_start[1] == central_end[1] == 0
    assert peripheral_start[1] == peripheral_end[1] == 1
    print('lineas_central_periferica: misma_orientacion=(1,0,0); '
          'distancia_minima_al_centro=0_vs_1')


if __name__ == '__main__':
    main()
