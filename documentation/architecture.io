<mxfile host="65bd71144e">
    <diagram id="D7kMozoIHEmUrMjNEDKK" name="architecture-high-level">
        <mxGraphModel dx="790" dy="494" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
                <mxCell id="2" value="DB" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;" vertex="1" parent="1">
                    <mxGeometry x="540" y="130" width="60" height="80" as="geometry"/>
                </mxCell>
                <mxCell id="11" value="" style="edgeStyle=none;html=1;" edge="1" parent="1" source="5" target="2">
                    <mxGeometry relative="1" as="geometry"/>
                </mxCell>
                <mxCell id="5" value="Webserver" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
                    <mxGeometry x="340" y="130" width="150" height="85" as="geometry"/>
                </mxCell>
                <mxCell id="6" value="Client" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
                    <mxGeometry x="140" y="130" width="40" height="90" as="geometry"/>
                </mxCell>
                <mxCell id="7" value="" style="curved=1;endArrow=classic;html=1;" edge="1" parent="1">
                    <mxGeometry width="50" height="50" relative="1" as="geometry">
                        <mxPoint x="190" y="160" as="sourcePoint"/>
                        <mxPoint x="330" y="160" as="targetPoint"/>
                        <Array as="points">
                            <mxPoint x="290" y="150"/>
                        </Array>
                    </mxGeometry>
                </mxCell>
                <mxCell id="14" value="HTTP" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];" vertex="1" connectable="0" parent="7">
                    <mxGeometry x="-0.0299" y="1" relative="1" as="geometry">
                        <mxPoint as="offset"/>
                    </mxGeometry>
                </mxCell>
                <mxCell id="8" value="" style="curved=1;endArrow=classic;html=1;" edge="1" parent="1">
                    <mxGeometry width="50" height="50" relative="1" as="geometry">
                        <mxPoint x="320" y="210" as="sourcePoint"/>
                        <mxPoint x="190" y="200" as="targetPoint"/>
                        <Array as="points">
                            <mxPoint x="250" y="215"/>
                        </Array>
                    </mxGeometry>
                </mxCell>
                <mxCell id="15" value="WebSockets" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];" vertex="1" connectable="0" parent="8">
                    <mxGeometry x="-0.0829" y="-4" relative="1" as="geometry">
                        <mxPoint as="offset"/>
                    </mxGeometry>
                </mxCell>
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>