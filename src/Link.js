import React from 'react';
import {css} from 'glamor';

export default function Link(props) {
    return <span {...css({
        color: 'blue',
        ':hover': {
            textDecoration: 'underline',
            cursor: 'pointer',
        }
    })} {...props}>{props.children}</span>;
}