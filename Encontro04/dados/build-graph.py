import os

from unidecode import unidecode


GRAPH_NAME = 'spotify'

DATA_DIR = 'data'

ROOT_DEPTH = 1

ROOT_NAME = 'Black Sabbath'
ROOT_UID = '5M52tdBnJaKSvOpJGz8mfZ'

DIRECTED = True

GRAPH_DIR = 'graph'


def load_successors(uid, depth=1, names=None):
    successors = set()

    path = os.path.join(DATA_DIR, GRAPH_NAME, uid + '.txt')

    try:
        with open(path, encoding='utf-8') as file:
            for line in file:
                words = line.split()

                if words:
                    successor = words[0]

                    successors.add(successor)

                    if names is not None and len(words) > 1:
                        names[successor] = unidecode(' '.join(words[1:]))
    except FileNotFoundError:
        pass

    if depth > 1:
        successors_copy = successors.copy()

        for successor in successors_copy:
            successors |= load_successors(uid, depth - 1, names)

    return successors


def main():
    names = {}
    successors = load_successors(ROOT_UID, ROOT_DEPTH, names)

    if ROOT_UID in successors:
        successors.remove(ROOT_UID)
    else:
        names[ROOT_UID] = ROOT_NAME

    uids = [ROOT_UID]
    uids.extend(successors)

    edges = []

    for n, uid in enumerate(uids):
        successors = load_successors(uid)

        for successor in successors:
            try:
                m = uids.index(successor)
            except ValueError:
                continue

            edges.append((n, m))

    if not DIRECTED:
        edges = [(n, m) for n, m in edges if n < m and (m, n) in edges]

    path = os.path.join(GRAPH_DIR, GRAPH_NAME + '.gml')

    with open(path, 'w') as file:
        file.write('graph [\n')
        file.write('  directed {}\n'.format(int(DIRECTED)))

        for i, uid in enumerate(uids):
            file.write('  node [\n')
            file.write('    id {}\n'.format(i))
            if uid in names:
                label = names[uid]
            else:
                label = uid
            file.write('    label "{}"\n'.format(label))
            file.write('  ]\n')

        for i, j in edges:
            file.write('  edge [\n')
            file.write('    source {}\n'.format(i))
            file.write('    target {}\n'.format(j))
            file.write('  ]\n')

        file.write(']\n')


if __name__ == '__main__':
    main()
