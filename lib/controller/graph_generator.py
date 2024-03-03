from lib.components.shapes import ShapeFactory


def generate_graphs(controller, dim, facet):
    from lib.fss.fss_output_parser import parse_output
    controller.get_labels()
    output = parse_output(controller.output_path)
    graph_data_list = []
    axes = list(range(dim))
    axes_pairs = [(a, b) for idx, a in enumerate(axes) for b in
                  axes[idx + 1:]]
    for a, b in axes_pairs:
        coors = output["dimensions"][dim]["coordinates"]
        x = [point['coordinates'][a] for point in coors]
        y = [point['coordinates'][b] for point in coors]
        index = [point['serial_number'] for point in coors]
        labels = [controller.var_labels[i - 1] for i in index]
        legend = [dict(index=index[i], value=labels[i]) for i in range(len(
            index))]
        graph = dict(
            x=x,
            y=y,
            annotations=index,
            title=f"FSS Solution d={dim} {a + 1}X{b + 1}",
            legend=legend
        )
        graph_data_list.append(graph)
        if facet is not None:
            index = [point['serial_number'] for point in coors]
            annotations = [controller.facet_var_details[i - 1][
                               facet - 1] for i in index]
            legend = [
                dict(index=i + 1, value=controller.facet_details[facet - 1][i])
                for i in range(len(controller.facet_details[facet - 1]))]
            graph = dict(
                x=x,
                y=y,
                annotations=annotations,
                title=f"Facet {chr(64 + facet)}: d={dim} {a + 1}X{b + 1}",
                legend=legend,
            )
            if dim == 2:
                for model in output["models"]:
                    if model["facet"] != facet: continue
                    m_graph = dict(x=x,
                                   y=y,
                                   annotations=annotations,
                                   title=f"Facet {chr(64 + facet)}: d={dim} {a + 1}X{b + 1}",
                                   legend=legend)
                    m_graph["geoms"] = ShapeFactory.shapes_from_list(model[
                                                                         "divide_geoms"])
                    m_graph["caption"] = f"Separation index for" \
                                         f" {model['deviant_points_num']} Deviant " \
                                         f"Points Is  {model['seperation_index']}"
                    graph_data_list.append(m_graph)
            else:
                graph_data_list.append(graph)
    return graph_data_list