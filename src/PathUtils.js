export default class PathUtils {
    join(a, b) {
        return a ? `${a}/${b}` : b;
    }
}