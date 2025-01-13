import { useParams } from 'react-router-dom';

function EnquiryDetail() {
  const { id } = useParams();
  return (
    <div>
      <h1>Enquiry Detail</h1>
      <p>Details for enquiry ID: {id}</p>
    </div>
  );
}

export default EnquiryDetail;
