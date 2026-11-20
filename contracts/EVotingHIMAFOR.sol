// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Library standar NFT ERC-721
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";


contract EVotingHIMAFOR is ERC721 {

    // =====================================================
    // STRUCT
    // =====================================================

    struct Candidate {
        uint256 id;
        string name;
        string vision;
        string mission;
        uint256 voteCount;
    }

    struct Voter {
        bool registered;
        bool verified;
        bool hasVoted;
    }


    // =====================================================
    // STATE VARIABLES
    // =====================================================

    address public admin;

    bool public electionOpen;

    uint256 public candidateCount;

    // Data pemilih berdasarkan address
    mapping(address => Voter) public voters;

    // Data kandidat berdasarkan ID
    mapping(uint256 => Candidate) public candidates;

    // Daftar ID kandidat
    uint256[] public candidateIds;


    // =====================================================
    // NFT VARIABLES
    // =====================================================

    // Token ID berikutnya
    uint256 public nextTokenId;

    // Data project/aset yang terhubung dengan NFT
    mapping(uint256 => string) public nftProjectData;


    // =====================================================
    // EVENTS
    // =====================================================

    event CandidateRegistered(
        uint256 candidateId,
        string name
    );

    event VoterRegistered(
        address voter
    );

    event VoterVerified(
        address voter
    );

    event ElectionOpened();

    event VoteCast(
        address voter,
        uint256 candidateId
    );

    event ElectionClosed();

    event VotingNFTMinted(
        address voter,
        uint256 tokenId
    );


    // =====================================================
    // MODIFIER
    // =====================================================

    modifier onlyAdmin() {
        require(
            msg.sender == admin,
            "Hanya admin yang dapat melakukan fungsi ini"
        );
        _;
    }


    // =====================================================
    // CONSTRUCTOR
    // =====================================================

    constructor()
        ERC721("HIMAFOR Voting Certificate", "HVC")
    {
        admin = msg.sender;

        electionOpen = false;

        nextTokenId = 1;
    }


    // =====================================================
    // 1. REGISTRASI KANDIDAT
    // =====================================================

    function registerCandidate(
        string calldata _name,
        string calldata _vision,
        string calldata _mission
    )
        external
        onlyAdmin
    {
        require(
            !electionOpen,
            "Tidak dapat mendaftarkan kandidat saat pemilihan berlangsung"
        );

        require(
            bytes(_name).length > 0,
            "Nama kandidat tidak boleh kosong"
        );

        candidateCount++;

        candidates[candidateCount] = Candidate({
            id: candidateCount,
            name: _name,
            vision: _vision,
            mission: _mission,
            voteCount: 0
        });

        candidateIds.push(candidateCount);

        emit CandidateRegistered(
            candidateCount,
            _name
        );
    }


    // =====================================================
    // 2. REGISTRASI PEMILIH
    // =====================================================

    function registerVoter(
        address _voter
    )
        external
        onlyAdmin
    {
        require(
            !electionOpen,
            "Tidak dapat mendaftarkan pemilih saat pemilihan berlangsung"
        );

        require(
            _voter != address(0),
            "Alamat pemilih tidak valid"
        );

        require(
            !voters[_voter].registered,
            "Pemilih sudah terdaftar"
        );

        voters[_voter].registered = true;

        emit VoterRegistered(_voter);
    }


    // =====================================================
    // 3. VERIFIKASI PEMILIH
    // =====================================================

    function verifyVoter(
        address _voter
    )
        external
        onlyAdmin
    {
        require(
            voters[_voter].registered,
            "Pemilih belum terdaftar"
        );

        voters[_voter].verified = true;

        emit VoterVerified(_voter);
    }


    // =====================================================
    // 4. MEMBUKA PEMILIHAN
    // =====================================================

    function openElection()
        external
        onlyAdmin
    {
        require(
            candidateCount > 0,
            "Belum ada kandidat"
        );

        require(
            !electionOpen,
            "Pemilihan sudah dibuka"
        );

        electionOpen = true;

        emit ElectionOpened();
    }


    // =====================================================
    // 5 & 6. VOTING + PENCEGAHAN DOUBLE VOTING
    // =====================================================

    function vote(
        uint256 _candidateId
    )
        external
    {
        // Pemilihan harus dibuka
        require(
            electionOpen,
            "Pemilihan belum dibuka"
        );

        // Pemilih harus terdaftar
        require(
            voters[msg.sender].registered,
            "Anda belum terdaftar sebagai pemilih"
        );

        // Pemilih harus diverifikasi
        require(
            voters[msg.sender].verified,
            "Pemilih belum diverifikasi"
        );

        // Mencegah double voting
        require(
            !voters[msg.sender].hasVoted,
            "Anda sudah melakukan voting"
        );

        // Kandidat harus valid
        require(
            _candidateId > 0 &&
            _candidateId <= candidateCount,
            "Kandidat tidak valid"
        );


        // ---------------------------------------------
        // MENAMBAHKAN SUARA
        // ---------------------------------------------

        candidates[_candidateId].voteCount++;


        // Menandai pemilih sudah voting
        voters[msg.sender].hasVoted = true;


        // ---------------------------------------------
        // MINT NFT BUKTI PARTISIPASI
        // ---------------------------------------------

        uint256 tokenId = nextTokenId;

        nextTokenId++;


        // Membuat NFT dan memberikannya kepada pemilih
        _safeMint(
            msg.sender,
            tokenId
        );


        // Data yang terhubung dengan NFT
        nftProjectData[tokenId] =
            "Bukti Partisipasi Voting HIMAFOR 2026";


        emit VoteCast(
            msg.sender,
            _candidateId
        );

        emit VotingNFTMinted(
            msg.sender,
            tokenId
        );
    }


    // =====================================================
    // 7. MENUTUP PEMILIHAN
    // =====================================================

    function closeElection()
        external
        onlyAdmin
    {
        require(
            electionOpen,
            "Pemilihan belum dibuka"
        );

        electionOpen = false;

        emit ElectionClosed();
    }


    // =====================================================
    // 8. MENAMPILKAN HASIL
    // =====================================================

    function getResults()
        external
        view
        returns (
            uint256[] memory ids,
            string[] memory names,
            uint256[] memory votes
        )
    {
        require(
            !electionOpen,
            "Hasil belum dapat dilihat sebelum pemilihan ditutup"
        );

        uint256 total = candidateIds.length;

        ids = new uint256[](total);
        names = new string[](total);
        votes = new uint256[](total);

        for (
            uint256 i = 0;
            i < total;
            i++
        ) {

            uint256 id = candidateIds[i];

            ids[i] = candidates[id].id;

            names[i] = candidates[id].name;

            votes[i] = candidates[id].voteCount;
        }

        return (
            ids,
            names,
            votes
        );
    }


    // =====================================================
    // MELIHAT DATA KANDIDAT
    // =====================================================

    function getCandidate(
        uint256 _candidateId
    )
        external
        view
        returns (
            uint256 id,
            string memory name,
            string memory vision,
            string memory mission,
            uint256 voteCount
        )
    {
        require(
            _candidateId > 0 &&
            _candidateId <= candidateCount,
            "Kandidat tidak ditemukan"
        );

        Candidate memory candidate =
            candidates[_candidateId];

        return (
            candidate.id,
            candidate.name,
            candidate.vision,
            candidate.mission,
            candidate.voteCount
        );
    }


    // =====================================================
    // CEK STATUS PEMILIH
    // =====================================================

    function getVoterStatus(
        address _voter
    )
        external
        view
        returns (
            bool registered,
            bool verified,
            bool hasVoted
        )
    {
        Voter memory voter =
            voters[_voter];

        return (
            voter.registered,
            voter.verified,
            voter.hasVoted
        );
    }


    // =====================================================
    // MELIHAT DATA NFT / ASET PROJECT
    // =====================================================

    function getNFTProjectData(
        uint256 _tokenId
    )
        external
        view
        returns (
            address owner,
            string memory projectData
        )
    {
        owner = ownerOf(_tokenId);

        projectData = nftProjectData[_tokenId];

        return (
            owner,
            projectData
        );
    }
}