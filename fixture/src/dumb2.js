sssssssconst fs = require("fs");

class AuctionModel {
  constructor(path) {
    this._path = path;
  }
  save(auctions) {
    if (!auctions || !auctions.length) {
      return;
    }

    const auctionsString = JSON.stringify(auctions);
    fs.writeFileSync(this._path, auctionsString);
  }
  clear() {
    if (this.exists()) return;

    fs.unlinkSync(this._path);
  }
  find() {
    if (!this.exists()) return [];

    const auctionsString = fs.readFileSync(this._path, "utf8");
    const auctions = JSON.parse(auctionsString);
    return auctions;
  }
  exists() {
    return fs.existsSync(this._path);
  }
  get path() {
    return this._path;
  }
}

const auctions = [
  {
    auctionUrl: "www.com.br",
    data: "2017-03-12",
    tiragem: 100000,
    preco: 23.5
  },
  {
    auctionUrl: "www.br.uk",
    data: "2019-09-01",
    tiragem: 1000,
    preco: 66.5
  },
  {
    auctionUrl: "www.hi.uk",
    data: "2019-03-01",
    tiragem: 9999,
    preco: 25
  },
  {
    auctionUrl: "www.nani.jp",
    data: "2015-11-01",
    tiragem: 9199,
    preco: 10
  }
];

const auctionModel = new AuctionModel("teste.json");

auctionModel.clear();
auctionModel.save(auctions);

const result = auctionModel.find();

result.sort((a, b) => (a.data < b.data ? -1 : a.data > b.data ? 1 : 0));

console.log(auctionModel.path);
