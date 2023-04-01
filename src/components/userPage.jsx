import React from 'react';
import Widget from "./Widget";
import ChartsGrid from "./ChartsGrid";
import Navbar from "./Navbar";
import Footer from "./Footer";
import TableRFM from "./TableRFM";

export default function UserPage() {
  return (
    <div>
        <Navbar />
        <Widget/>
        <ChartsGrid/>
        <TableRFM />
        <Footer/>
    </div>
  )
}
