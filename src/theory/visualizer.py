from typing import *
from src.theory import *
from loguru import logger

import graphviz


class Visualizer:

    def __init__(self, settings:dict) -> None:
        self._settings = settings   

    def _build_from_song(self, song: Song) -> graphviz.Digraph:
        super_graph = graphviz.Digraph("Your Song", graph_attr={'rankdir':'LR'})

        idx_offset = 0
        for idx, section in enumerate(song.sections):
            # Build sub graphs, link together
            sect = self._build_from_seq(
                name=f"Sequence {idx+1}" if not section.designation else section.designation, 
                sequence=section,
                index_offset=idx_offset
            )
            # sect_graphs.append(sect)
            super_graph.subgraph(sect)
            idx_offset = idx_offset + len(section)
        return super_graph

    def _build_from_seq(self, name:str, sequence:Union[ChordProgression, Scale, NoteSequence], index_offset:int=0, detail_level:int=0) -> graphviz.Digraph:
        graph = graphviz.Digraph(name, graph_attr={'rankdir':'LR'})
        edges = []
        prev_ch = None

        for idx, ele in enumerate(sequence):
            node_id = ele.__str__().replace(" ", "")
            if detail_level == 0 :
                ele_str = ele.__str__()
            elif detail_level == 1:
                ele_str = ele.__repr__().replace("")

            graph.node(
                str(index_offset + idx),
                ele_str.strip(),
                shape='square'
            )
            if prev_ch:
                edges.append(f"{index_offset + idx-1}{index_offset + idx}")

            prev_ch = node_id


        edges.append(f"{index_offset + len(sequence) - 1}{index_offset}")
        graph.edges(edges)
        return graph



if __name__ == "__main__":
    from src.tests.artifacts.songs import song_one
    viz = Visualizer({})
    logger.debug(song_one)
    graph = viz._build_from_song(
        song_one
    )
    graph.view()