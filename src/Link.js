import React from 'react';
import {css} from 'glamor';

export default function Link(props) {
    return <span {...css({
        color: 'blue',
    })} onClick={props.onClick}>{props.children}</span>;
}