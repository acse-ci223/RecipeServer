

__all__ = ['Grapher']


class Grapher:
    def __init__(self):
        pass

    def graph(self, recipe):

        mermaid_graph = "flowchart TD\n\n"

        subgraphs = []

        recipe = recipe[0]

        for step in recipe.keys():
            step_number = step
            step = dict(recipe[step])
            time = step.get('time', [1, 1])
            step_instruction = step.get('step_instruction', [])

            t = "{} to {} mins".format(time[0], time[1]) if time[0] != time[1] != 0 else f"{time[0]} mins"

            mermaid_graph += "subgraph step_{}[Step {} - {}]\n".format(step_number, step_number, t)

            instructions = []

            for instruction in step_instruction:
                instruction_object = dict(step_instruction[instruction])
                instruction_description = instruction_object.get('instruction',
                                                                 '')
                instruction_time = instruction_object.get('time', [0, 0])

                t = "{} to {} mins".format(instruction_time[0], instruction_time[1]) if instruction_time[0] != instruction_time[1] != 0 else f"{instruction_time[0]} mins"

                mermaid_graph += 'step_{}_sub{}("`{} \n\n Approximate time - {}`") \n'.format(step_number,
                                                                    instruction,
                                                                    instruction_description,
                                                                    t)

                instructions.append("step_{}_sub{}".format(step_number,
                                                           instruction))

            mermaid_graph += " --> ".join(instructions)
            mermaid_graph += "\n"

            mermaid_graph += "end\n"

            subgraphs.append("step_{}".format(step_number))

        mermaid_graph += "\n"
        mermaid_graph += " --> ".join(subgraphs)

        self.save(mermaid_graph, "sample.md")

        return mermaid_graph

    def save(self, mermaid_graph, filename):
        mermaid_graph = """```mermaid\n{}\n```""".format(mermaid_graph)
        with open(filename, 'w') as file:
            file.write(mermaid_graph)
