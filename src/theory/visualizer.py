from typing import *
from src.theory import *
from loguru import logger

import graphviz


class Visualizer:

    def __init__(self, settings:dict) -> None:
        self._settings = settings if settings else {
            'rankdir':'LR',
            'bgcolor': '#0e1117',
            'color': 'blue',
            'fontcolor': 'white'
        }

    def _build_from_song(self, song: Song) -> graphviz.Digraph:
        if song.is_empty():
            return None
        super_graph = graphviz.Digraph(
            song.title if song.title else "Song Chords", 
            graph_attr=self._settings
        )

        idx_offset = 0
        # For some reason idk I need to do the adding to supergraph in reverse
        # Graphvize adds bottom up? I guess.
        for idx, section in enumerate(reversed(song.sections)):
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
        graph = graphviz.Digraph(
            name,
            graph_attr=self._settings
        )

        prev_ch = None
        first_node = None
        for idx, ele in enumerate(sequence):
            node_id = str(index_offset + idx)

            if detail_level == 0 :
                ele_str = ele.__str__()
            elif detail_level == 1:
                ele_str = ele.__repr__().replace("")

            graph.node(
                node_id,
                ele_str.strip(),
                shape='square',
                color="cyan3",
                fontcolor="white",
                fillcolor="white",
                style="rounded"
            )   
            if prev_ch:
                graph.edge(
                    prev_ch, node_id, color="grey"
                )
            else:
                first_node = node_id
            prev_ch = node_id

        graph.edge(
            prev_ch, 
            first_node, 
            color="grey"
        )
        return graph



if __name__ == "__main__":
    from src.tests.artifacts.songs import song_one
    viz = Visualizer(None)
    logger.debug(song_one)
    graph = viz._build_from_song(
        song_one
    )
    graph.view()