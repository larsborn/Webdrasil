import React from 'react';
import Link from "./Link";

export default function DirLink(props) {
    return <Link onMouseDown={(event) => {
        if (event.button === 1) {
            event.preventDefault();
        }
    }} onMouseUp={(event) => {
        switch (event.button) {
            case 0: // left
                props.loadFunc(props.dir);
                break;
            case 1: // middle
                window.open(window.location.href.match(/(^[^#]*)/)[0] + '#' + props.dir, '_blank');
                event.preventDefault();
                break;
            default:
                break
        }
    }}>{props.caption}</Link>
}